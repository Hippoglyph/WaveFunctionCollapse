from PIL import Image, ImageTk
import tkinter as tk

from tile import Direction, Tile

class Canvas:

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Wave Form Collapse")
        self.window_width = 500
        self.window_height = 500
        self.canvas = tk.Canvas(self.window, width=self.window_width, height=self.window_height)
        self.canvas.pack()
        
    def _create_image(self, image: Image) -> None:
        self.canvas.delete("all")
        # Resize the image
        resized_image = image.resize((self.window_width, self.window_height), Image.Resampling.NEAREST)
        
        # Convert the resized image to a format that Tkinter can use
        tk_image = ImageTk.PhotoImage(resized_image)


        # Create a canvas and draw the resized image on it
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        
        # Keep a reference to prevent garbage collection
        self.canvas.image = tk_image
        self.window.update_idletasks()



    def render_image(self, img_path : str) -> None:
        """
        Render an image from a file path.
        """
        # Open the image using PIL
        image = Image.open(img_path)
        
        self._create_image(image)

    def render_tiles(self, tiles : list[Tile]) -> None:
        """
        Render an image from a list of lists of RGB tuples.
        """
        images = []
        for tile in tiles:
            image = self._create_tile_image(tile)
            images.append(image)

        # Calculate the total width of all images
        total_width = sum(image.width for image in images)
        max_height = max(image.height for image in images)

        # Create a new image to hold all the images side by side
        combined_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0

        # Paste each image into the combined image
        for image in images:
            combined_image.paste(image, (x_offset, (max_height - image.height) // 2))
            x_offset += image.width

        self._create_image(combined_image)

    def render_neighbour(self, tile : Tile) -> None:
        """
        Render an image from a list of lists of RGB tuples.
        """

        source_image = self._create_tile_image(tile)
        east_images = []
        for neighbour in tile.get_tiles(Direction.EAST):
            image = self._create_tile_image(neighbour)
            east_images.append(image)

        south_images = []
        for neighbour in tile.get_tiles(Direction.SOUTH):
            image = self._create_tile_image(neighbour)
            south_images.append(image)

        west_images = []
        for neighbour in tile.get_tiles(Direction.WEST):
            image = self._create_tile_image(neighbour)
            west_images.append(image)

        north_images = []
        for neighbour in tile.get_tiles(Direction.NORTH):
            image = self._create_tile_image(neighbour)
            north_images.append(image)

        # Calculate the total width of all images
        total_width = sum(image.width for image in west_images) + source_image.width + sum(image.width for image in east_images)
        total_height = sum(image.height for image in north_images) + source_image.height + sum(image.height for image in south_images)

        # Create a new image to hold all the images side by side
        combined_image = Image.new('RGB', (total_width, total_height))

        x_offset_source = sum(source_image.width for image in west_images)
        y_offset_source = sum(source_image.height for image in north_images)

        combined_image.paste(source_image, (x_offset_source, y_offset_source))

        x_offset = 0
        for image in west_images:
            x_offset += image.width
            combined_image.paste(image, (x_offset_source - x_offset, y_offset_source))

        x_offset = 0
        for image in east_images:
            x_offset += image.width
            combined_image.paste(image, (x_offset_source + x_offset, y_offset_source))

        y_offset = 0
        for image in north_images:
            y_offset += image.height
            combined_image.paste(image, (x_offset_source, y_offset_source - y_offset))

        y_offset = 0
        for image in south_images:
            y_offset += image.height
            combined_image.paste(image, (x_offset_source, y_offset_source + y_offset))

        self._create_image(combined_image)

    def _create_tile_image(self, tile : Tile, padding_scaler : int = 1) -> Image:
        height = len(tile.pixels)
        width = len(tile.pixels[0])

        # Create an image from the matrix
        image = Image.new('RGB', (width + 2 * padding_scaler, height + 2 * padding_scaler), (255, 0, 0))
        pixels = image.load()

        # Populate the image with pixels from the matrix
        for row, col in enumerate(tile.pixels):
            for x, pixel in enumerate(col):
                r = pixel[0]
                b = pixel[1]
                g = pixel[2]
                if r < 0 or b < 0 or g < 0:
                    r = 200
                    b = 100
                    g = 50
                pixels[x + 1 * padding_scaler, row + 1 * padding_scaler] = (r,b,g)
        return image
    
    def render_color_grid(self, grid = list[list[tuple[int]]]) -> None:
        combined_image = Image.new('RGB', (len(grid), len(grid[0])))
        pixels = combined_image.load()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pixels[j,i] = grid[i][j]
        self._create_image(combined_image)

