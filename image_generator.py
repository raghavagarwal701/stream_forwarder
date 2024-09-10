import asyncio
from score_fetch import fetch_match_data
from PIL import Image, ImageDraw, ImageFont

def main():
    match_id = "99gopm8z7m"
    score = fetch_match_data(match_id)
    print(score)

    # Open the sample image
    img = Image.open('sampleimage.png')
    draw = ImageDraw.Draw(img)

    # Load custom font (if available, otherwise default font)
    font_path = "OpenSans-Regular.ttf"  # Change this to the path of a .ttf font file if you want to use one
    default_font_size = 20
    try:
        font = ImageFont.truetype(font_path, default_font_size)
    except IOError:
        font = ImageFont.load_default()

    # Define score details with their specific coordinates and font sizes
    score_elements = [
        {"text": f"{score['batting_team']}", "position": (230, 3), "font_size": 44},
        {"text": f"{score['bowling_team']}", "position": (1800, 3), "font_size": 44},
        {"text": f"{score['score']}", "position": (1000, 60), "font_size": 54},
        {"text": f"{score['overs_bowled']} ", "position": (1120, 80), "font_size": 34},
        {"text": f"{score['batter_one']}:  {score['batter_one_score']['runs']}({score['batter_one_score']['balls']})", "position": (85, 70), "font_size": 35},
        {"text": f"{score['batter_two']}:  {score['batter_two_score']['runs']}({score['batter_two_score']['balls']})", "position": (85, 130), "font_size": 35},
        {"text": f"{score['bowler']} - {score['bowler_figure']['runsGiven']}/{score['bowler_figure']['wickets']} in {score['bowler_figure']['ballsDelivered']} balls", "position": (1650, 100), "font_size": 40}
    ]

    # Loop through score elements and add each to the image
    for element in score_elements:
        # Adjust font size if specified
        font = ImageFont.truetype(font_path, element["font_size"]) if font_path else ImageFont.load_default()
        
        # Add the text to the image at the specified position
        draw.text(element["position"], element["text"], font=font, fill="white")

    # Save the modified image with match_id as the filename
    img.save(f'{match_id}.png')

    print(f"Image saved as {match_id}.png")

main()
