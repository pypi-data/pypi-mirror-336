import torch
import lightning as L

class Dataset(L.LightningDataModule):
    def __init__(self, ds, input_vns, output_vns, train_frac=0.7, val_frac=0.1, test_frac=0.2,
                 x_mean=None, x_std=None, y_mean=None, y_std=None, batch_size=128, num_workers=4):
        super().__init__()
        self.ds = ds
        self.input_vns = input_vns
        self.output_vns = output_vns
        self.batch_size = batch_size
        self.num_workers = num_workers

        assert abs(train_frac + val_frac + test_frac - 1.0) < 1e-6, 'Train, val, and test fractions must sum to 1.'
        self.train_frac = train_frac
        self.val_frac = val_frac
        self.test_frac = test_frac

        # Allow external mean and std
        self.x_mean = x_mean
        self.x_std = x_std
        self.y_mean = y_mean
        self.y_std = y_std

    def setup(self, stage=None):
        x = torch.stack([torch.from_numpy(self.ds[vn].values) for vn in self.input_vns], dim=1)
        y = torch.stack([torch.from_numpy(self.ds[vn].values) for vn in self.output_vns], dim=1)
        dataset = torch.utils.data.TensorDataset(x, y)

        # Compute dataset indices
        ds_idx = list(range(len(dataset)))
        test_size = int(len(dataset) * self.test_frac)
        train_valid_size = len(dataset) - test_size
        
        # Split train+val and test sets
        self.train_valid_idx = ds_idx[:train_valid_size]
        self.test_idx = ds_idx[train_valid_size:]
        
        train_valid_set = torch.utils.data.Subset(dataset, self.train_valid_idx)
        self.test_set = torch.utils.data.Subset(dataset, self.test_idx)
        
        # Further split into train and validation sets
        train_size = int(self.train_frac / (self.train_frac + self.val_frac) * train_valid_size)
        val_size = train_valid_size - train_size
        self.train_set, self.valid_set = torch.utils.data.random_split(train_valid_set, [train_size, val_size])

        # If mean/std not provided, compute from training set
        if self.x_mean is None or self.x_std is None:
            train_x = torch.stack([self.train_set[i][0] for i in range(len(self.train_set))])
            self.x_mean, self.x_std = train_x.mean(dim=0), train_x.std(dim=0)

        if self.y_mean is None or self.y_std is None:
            train_y = torch.stack([self.train_set[i][1] for i in range(len(self.train_set))])
            self.y_mean, self.y_std = train_y.mean(), train_y.std()

        # Normalize datasets using specified or computed statistics
        self.train_set = self.normalize_subset(self.train_set)
        self.valid_set = self.normalize_subset(self.valid_set)
        self.test_set = self.normalize_subset(self.test_set)

    def normalize_subset(self, subset):
        normalized_data = []
        for i in range(len(subset)):
            x, y = subset[i]
            x = (x - self.x_mean) / self.x_std
            y = (y - self.y_mean) / self.y_std
            normalized_data.append((x, y))
        return normalized_data

    def denormalize(self, y_hat):
        """Convert predictions back to original scale."""
        return y_hat * self.y_std + self.y_mean

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.train_set, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.valid_set, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_set, batch_size=self.batch_size, num_workers=self.num_workers)
