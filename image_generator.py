import asyncio
from score_fetch import fetch_match_data
from PIL import Image, ImageDraw, ImageFont

def main():
    match_id = "99gopm8z7m"
    score = fetch_match_data(match_id)
    print(score)

    # Open the sample image
    img = Image.open('score_image.png')
    draw = ImageDraw.Draw(img)

    # Load custom font (if available, otherwise default font)
    font_path = "OpenSans-Regular.ttf"  # Change this to the path of a .ttf font file if you want to use one
    default_font_size = 20
    try:
        font = ImageFont.truetype(font_path, default_font_size)
    except IOError:
        font = ImageFont.load_default()

    batting_team_text_width = len(score['batting_team']) * 10
    # Define score details with their specific coordinates and font sizes
    score_elements = [
        {"text": f"{score['batting_team']}", "position": (35, 3), "font_size": 23},
        {"text": f"{score['bowling_team']}", "position": (35, 45), "font_size": 23},
        {"text": f"{score['score']}", "position": (35 + batting_team_text_width + 30, 6), "font_size": 20, "color": '#FFCB05'},
        {"text": f"{score['overs_bowled']} ", "position": (150, 14), "font_size": 14},
        {"text": f"{score['batter_one']}:  {score['batter_one_score']['runs']}({score['batter_one_score']['balls']})", "position": (325, 10), "font_size": 20},
        {"text": f"{score['batter_two']}:  {score['batter_two_score']['runs']}({score['batter_two_score']['balls']})", "position": (325, 45), "font_size": 20},
        {"text": f"{score['bowler']}", "position": (629, 23), "font_size": 20},
        {"text": f"{score['bowler_figure']['ballsDelivered']}", "position": (757, 23), "font_size": 20},
        {"text": f"balls", "position": (750, 49), "font_size": 12},
        {"text": f"{score['bowler_figure']['runsGiven']}", "position": (802, 23), "font_size": 20},
        {"text": f"runs", "position": (798, 49), "font_size": 12},
        {"text": f"{score['bowler_figure']['wickets']}", "position": (855, 23), "font_size": 20},
        {"text": f"wickets", "position": (840, 49), "font_size": 12},
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
