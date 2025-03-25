"""
Implements several classes to transform images using the torchvision transforms framework
All transformations are not in-place to prevent the original image from being overwrited
"""
# from third party packages:
import torch
from torchvision import transforms
import numpy as np


class ToTensor(object):
    """ Converts ndarrays in a sample dictionary to Tensors. """

    def __init__(self, swap_color_axis=True):
        self.swap_color_axis = swap_color_axis

    def __call__(self, sample: dict):
        """
        convert a sample from numpy array to torch tensor
        :param sample (dict): contains numpy arrays with information relevant to the sample
        :return (dict): dictionary with the same keys and with torch tensor values
        """
        tensorized_sample = {}

        for k, v in sample.items():
            if k == "image" and self.swap_color_axis:
                # swap color axis because
                # numpy image: H x W x C
                # torch image: C x H x W
                if isinstance(v, torch.Tensor):
                    tensorized_sample[k] = torch.permute(v, (2, 0, 1))
                else:
                    tensorized_sample[k] = torch.from_numpy(v.transpose((2, 0, 1)))
            else:
                if isinstance(v, torch.Tensor):
                    tensorized_sample[k] = v
                else:
                    tensorized_sample[k] = torch.from_numpy(np.array(v))

        return tensorized_sample


class RandomGaussianNoise(object):
    """ Adds random gaussian noise to an image """

    def __init__(self, mean=0, stddev=0.1):
        """
        :param mean: float or int corresponding to the mean of the distribution
        :param stddev: float or int corresponding to the standard deviations of the distribution
        """
        self.mu = mean
        self.sigma = stddev

    def __call__(self, sample: dict):
        """
        Adds noise to the image in the given sample
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with a nosiy image
        """

        new_sample = {**sample}
        image_dims = sample["image"].shape
        mean = torch.zeros(image_dims) + self.mu
        stddev = torch.zeros(image_dims) + self.sigma
        new_sample["image"] = sample["image"] + torch.normal(mean, stddev).to(sample["image"].device)

        return new_sample


class RandomHorizontalFlip(object):
    """ Randomly flips and image horizontally """

    def __init__(self, p=0.5):
        """
        :param p: probability of randomly flipping the image
        """
        self.flipper = transforms.RandomHorizontalFlip(p=p)

    def __call__(self, sample: dict):
        """
        Randomly flips the image in a sample
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with a nosiy image
        """
        new_sample = {**sample}
        new_sample["image"] = self.flipper(sample["image"])
        return new_sample


class RandomVerticalFlip(object):
    """ Randomly flips and image horizontally """

    def __init__(self, p=0.5):
        """
        :param mean: float or int corresponding to the mean of the distribution
        :param stddev: float or int corresponding to the standard deviations of the distribution
        """
        self.flipper = transforms.RandomVerticalFlip(p=p)

    def __call__(self, sample: dict):
        """
        Randomly flips the image in a sample
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with a nosiy image
        """
        new_sample = {**sample}
        new_sample["image"] = self.flipper(sample["image"])
        return new_sample


class RandomRotator(object):
    """ Randomly rotates an image by certain number of degrees """

    def __init__(self, degrees=(0, 45)):
        """
        :param degrees: (tuple) range of degrees to randomly rotate to
        """
        self.rotator = transforms.RandomRotation(degrees=degrees)

    def __call__(self, sample: dict):
        """
        Randomly flips the image in a sample
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with a nosiy image
        """
        new_sample = {**sample}
        new_sample["image"] = self.rotator(sample["image"])
        return new_sample


class RandomCrop(object):
    """ Pads an image by a given number of pixels and then randomly crops the image to the original shape """

    def __init__(self, size: int, padding, padding_mode="reflect"):
        """
        :param size: (int or tuple) if int crops the image to (size, size), if tuple crops the image to (h, w) where h
                     and w are the first and second entry in the tuple
        :param padding (int or tuple): number of pixels to pad with on each side of the image
        :param padding_mode (str): padding mode (see torchvision documentation),
                                   options: "constant", "edge", "reflect", and "symmetric"
        """
        self.cropper = transforms.RandomCrop(size=size, padding=padding, padding_mode=padding_mode)

    def __call__(self, sample: dict):
        """
        Randomly flips the image in a sample
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with a nosiy image
        """
        new_sample = {**sample}
        new_sample["image"] = self.cropper(sample["image"])
        return new_sample


class RandomErasing(object):

    """ Erases a square at a random position in an image """
    def __init__(self, scale=(0.2, 0.33), ratio=(0.3, 3.3), value=0, swap_colors: bool = False):
        """
        Parameter descriptions as in: https://pytorch.org/vision/stable/transforms.html
        :param scale: (tuple, (float, float)) range of proportion of erased area against input image.
        :param ratio: (tuple, (float, float)) range of aspect ratio of erased area.
        :param value: (float) the replacement value for pixels or (3D tuple) with a replacement value for each channel
        :param swap_colors: (bool) whether to reshape from HxWxC to CxHxW when performing the transformation, only
                            relevant is value is a tuple
        """

        self.swap_colors = swap_colors
        self.eraser = transforms.RandomErasing(p=1.0, scale=scale, ratio=ratio, value=value, inplace=False)

    def __call__(self, sample: dict):
        """
        Zeros out a square in the image at a random position
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with an empty squared somewhere in the image
        """
        new_sample = {**sample}
        if self.swap_colors:
            new_image = torch.permute(new_sample["image"], (2, 0, 1))
            erased_image = self.eraser(new_image)
            new_sample["image"] = torch.permute(erased_image, (1, 2, 0))
        else:
            new_sample["image"] = self.eraser(new_sample["image"])
        return new_sample


class GrayScale(object):

    """ Transforms the image to a grayscale """
    def __init__(self, num_output_channels: int = 3, swap_colors: bool = False):
        """
        Parameter descriptions as in: https://pytorch.org/vision/stable/transforms.html
        :param num_output_channels: (int) number of expected output channels for the image
        :param swap_colors: (bool) whether to reshape from HxWxC to CxHxW when performing the transformation, only
                            relevant is value is a tuple
        """

        self.swap_colors = swap_colors
        self.grayscaler = transforms.Grayscale(num_output_channels=num_output_channels)

    def __call__(self, sample: dict):
        """
        Zeros out a square in the image at a random position
        :param sample: a dictionary that contains an "image" key corresponding to a torch tensor value
        :return: same dictionary as sample but with an empty squared somewhere in the image
        """
        new_sample = {**sample}
        if self.swap_colors:
            new_image = torch.permute(new_sample["image"], (2, 0, 1))
            grayscale_image = self.grayscaler(new_image)
            new_sample["image"] = torch.permute(grayscale_image, (1, 2, 0))
        else:
            new_sample["image"] = self.grayscaler(new_sample["image"])
        return new_sample


class Permute(object):

    """ Permutes all the pixels in an image according to the given index array"""
    def __init__(self, idx_array: np.ndarray):
        """
        :param idx_array (np array): array of permuted indices indicating how to permute images
        """
        self.permutation = idx_array

    def __call__(self, sample: dict):
        new_sample = {**sample}
        og_dims = sample["image"].shape
        flat_image = sample["image"].flatten()
        perm_flat_image = flat_image[self.permutation]
        new_sample["image"] = perm_flat_image.reshape(og_dims)
        return new_sample


class Normalize(object):

    """ Centers and scales each channel of an image by the given mean and standard deviation """
    def __init__(self, mean: tuple, std: tuple):
        """
        :param mean: tuple of means, one per channel
        :param std: tuple of standard deviations, one per channel
        """
        self.normalizer = transforms.Normalize(mean=mean, std=std)

    def __call__(self, sample: dict):
        new_sample = {**sample}
        normalize_image = self.normalizer(sample["image"])
        new_sample["image"] = normalize_image
        return new_sample




def main():
    import matplotlib.pyplot as plt

    def plot_image(image, title):
        plt.imshow(image)
        plt.title(title)
        plt.show()
        plt.close()

    # create and plot original image
    width = 400
    height = 600
    image = np.ones((width, height, 3), dtype=np.float32) * 0.5
    image[:np.random.randint(400), :np.random.randint(600), :] *= 0
    sample = {"image": image}
    plot_image(sample["image"], "Original")
    print("The type of the original image is:", type(image))
    print("The dimensions of the original image is:", image.shape, "\n")

    # test to tensor transformation
    totensor = ToTensor()
    tensorized_sample = totensor(sample)
    plot_image(tensorized_sample["image"].permute(1, 2, 0), "Tensorized")
    print("The type of the tensorized image is:", type(tensorized_sample["image"]))
    print("The dimensions of the tensorized image is:", tensorized_sample["image"].shape, "\n")

    # test adding gaussian noise
    gaussian_noise = RandomGaussianNoise(mean=0, stddev=0.1)
    noisy_sample = gaussian_noise(tensorized_sample)
    plot_image(noisy_sample["image"].permute(1, 2, 0), "Noisy")
    print("The type of the noisy image is:", type(noisy_sample["image"]))
    print("The dimensions of the noisy image is:", noisy_sample["image"].shape, "\n")
    plot_image(tensorized_sample["image"].permute(1, 2, 0), "Tensorized")

    # test adding a random black square
    eraser = RandomErasing(scale=(0.2, 0.3), ratio=(1,1))
    erased_sample = eraser(tensorized_sample)
    plot_image(erased_sample["image"].permute(1, 2, 0), "Erased")
    print("The type of the erased image is:", type(erased_sample["image"]))
    print("The dimensions of the erased image is:", erased_sample["image"].shape, "\n")
    plot_image(tensorized_sample["image"].permute(1, 2, 0), "Tensorized")

    # test adding noise and a square
    composite_transform = transforms.Compose([gaussian_noise, eraser])
    composite_sample = composite_transform(tensorized_sample)
    plot_image(composite_sample["image"].permute(1,2,0), "composite")
    print("The type of the composite image is:", type(composite_sample["image"]))
    print("The dimensions of the composite image is:", composite_sample["image"].shape, "\n")
    plot_image(tensorized_sample["image"].permute(1, 2, 0), "Tensorized")

    # test random permuatation
    num_pixels = width * height * 3
    rand_perm = np.random.permutation(num_pixels)
    permute_func = Permute(rand_perm)
    permuted_image = permute_func(tensorized_sample)
    plot_image(permuted_image["image"].permute(1,2,0), "permuted")
    print("The type of the permuted image is:", type(permuted_image["image"]))
    print("The dimensions of the permuted image is:", permuted_image["image"].shape, "\n")
    plot_image(tensorized_sample["image"].permute(1, 2, 0), "Tensorized")

    # plot original image again
    plot_image(sample["image"], "Original")
    print("The type of the original image is:", type(image))
    print("The dimensions of the original image is:", image.shape, "\n")


if __name__ == "__main__":
    main()
