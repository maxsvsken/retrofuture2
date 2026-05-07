from PIL import Image, ImageChops

def remove_background_and_crop(input_path, output_path):
    # Load image
    img = Image.open(input_path).convert("RGBA")
    
    # Data as list of pixels
    datas = img.getdata()
    
    newData = []
    # Define a threshold for white
    threshold = 240
    
    for item in datas:
        # item is (R, G, B, A)
        if item[0] >= threshold and item[1] >= threshold and item[2] >= threshold:
            # Replace white with transparent
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Get bounding box of non-transparent pixels to crop
    # Find the non-zero (non-transparent) area
    alpha = img.getchannel('A')
    bbox = alpha.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Save image
    img.save(output_path, "PNG")
    print(f"Processed image saved to {output_path}")

if __name__ == "__main__":
    input_file = r"c:\MySites\A1_PopArt 2\images\Логотипы СМИ для сайта\Логотипы СМИ для сайта\Forbes.png"
    output_file = r"c:\MySites\A1_PopArt 2\images\Логотипы СМИ для сайта\Логотипы СМИ для сайта\Forbes_no_bg.png"
    remove_background_and_crop(input_file, output_file)
