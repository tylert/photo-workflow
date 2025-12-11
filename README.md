# Photo Workflow

    x / y = r
    4 / 3 = 1.333333  # 4:3 aspect ratio

    # Chop off equal amounts of top and bottom pixels
    magick before_2250x4000.jpg -gravity center -crop 2250x3000+0+0 -quality 100 after_2250x3000.jpg
