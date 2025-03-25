import torch
import lightning as L

class SpectralConv2d(L.LightningModule):
    def __init__(self, in_channels, out_channels, modes1, modes2):
        super().__init__()
        """
        2D Fourier layer. It does FFT, linear transform, and Inverse FFT.
        """
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes1 = modes1  # Number of Fourier modes to multiply, at most floor(N/2) + 1
        self.modes2 = modes2

        self.scale = (1 / (in_channels * out_channels))
        self.weights1 = torch.nn.Parameter(
            self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, dtype=torch.cfloat))
        self.weights2 = torch.nn.Parameter(
            self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, dtype=torch.cfloat))

    # Complex multiplication
    def compl_mul2d(self, input, weights):
        # (batch, in_channel, x,y ), (in_channel, out_channel, x,y) -> (batch, out_channel, x,y)
        return torch.einsum("bixy,ioxy->boxy", input, weights)

    def forward(self, x):
        batchsize = x.shape[0]
        # Compute Fourier coeffcients up to factor of e^(- something constant)
        x_ft = torch.fft.rfft2(x)

        # Multiply relevant Fourier modes
        out_ft = torch.zeros(
            batchsize, self.out_channels, x.size(-2), x.size(-1) // 2 + 1,
            dtype=torch.cfloat, device=x.device,
        )
        out_ft[:, :, :self.modes1, :self.modes2] = self.compl_mul2d(x_ft[:, :, :self.modes1, :self.modes2], self.weights1)
        out_ft[:, :, -self.modes1:, :self.modes2] = self.compl_mul2d(x_ft[:, :, -self.modes1:, :self.modes2], self.weights2)

        # Return to physical space
        x = torch.fft.irfft2(out_ft, s=(x.size(-2), x.size(-1)))
        return x


class FNO2d(L.LightningModule):
    def __init__(self, modes1, modes2, width, weights=None):
        super().__init__()

        """
        The overall network. It contains 4 layers of the Fourier layer.
        1. Lift the input to the desire channel dimension by self.fc0 .
        2. 4 layers of the integral operators u' = (W + K)(u).
            W defined by self.w; K defined by self.conv .
        3. Project from the channel space to the output space by self.fc1 and self.fc2 .

        input: the solution of the coefficient function and locations (a(x, y), x, y)
        input shape: (batchsize, x=s, y=s, c=3)
        output: the solution
        output shape: (batchsize, x=s, y=s, c=1)
        """
        self.modes1 = modes1
        self.modes2 = modes2
        self.width = width
        self.weights = weights

        self.fc0 = torch.nn.Linear(2, self.width)

        self.conv0 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv1 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv2 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.conv3 = SpectralConv2d(self.width, self.width, self.modes1, self.modes2)
        self.w0 = torch.nn.Conv2d(self.width, self.width, 1)
        self.w1 = torch.nn.Conv2d(self.width, self.width, 1)
        self.w2 = torch.nn.Conv2d(self.width, self.width, 1)
        self.w3 = torch.nn.Conv2d(self.width, self.width, 1)

        self.fc1 = torch.nn.Linear(self.width, 128)
        self.fc2 = torch.nn.Linear(128, 1)

    def forward(self, x):
        x = x.permute(0, 2, 3, 1)

        x = self.fc0(x)
        x = x.permute(0, 3, 1, 2)

        x1 = self.conv0(x)
        x2 = self.w0(x)
        x = x1 + x2
        x = torch.nn.functional.relu(x)

        x1 = self.conv1(x)
        x2 = self.w1(x)
        x = x1 + x2
        x = torch.nn.functional.relu(x)

        x1 = self.conv2(x)
        x2 = self.w2(x)
        x = x1 + x2
        x = torch.nn.functional.relu(x)

        x1 = self.conv3(x)
        x2 = self.w3(x)
        x = x1 + x2

        x = x.permute(0, 2, 3, 1)
        x = self.fc1(x)
        x = torch.nn.functional.relu(x)
        x = self.fc2(x)

        x = x.permute(0, 3, 1, 2)

        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        if self.weights is not None:
            loss = torch.nn.functional.mse_loss(y_hat, y, reduction='none')
            loss = (loss*self.weights.view(1,1,-1,1)).mean()
        else:
            loss = torch.nn.functional.mse_loss(y_hat, y)

        self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        if self.weights is not None:
            loss = torch.nn.functional.mse_loss(y_hat, y, reduction='none')
            loss = (loss*self.weights.view(1,1,-1,1)).mean()
        else:
            loss = torch.nn.functional.mse_loss(y_hat, y)

        self.log('valid_loss', loss, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        if self.weights is not None:
            loss = torch.nn.functional.mse_loss(y_hat, y, reduction='none')
            loss = (loss*self.weights.view(1,1,-1,1)).mean()
        else:
            loss = torch.nn.functional.mse_loss(y_hat, y)

        self.log('test_loss', loss, sync_dist=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer