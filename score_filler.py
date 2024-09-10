from PIL import Image, ImageDraw, ImageFont
import io

def create_score_strip(score_data):
    # Create a new image with a blue background
    img = Image.new('RGB', (1120, 100), color='blue')
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_small = ImageFont.truetype("OpenSans-Regular.ttf", 16)
    font_medium = ImageFont.truetype("OpenSans-Regular.ttf", 20)
    font_large = ImageFont.truetype("OpenSans-Regular.ttf", 40)

    # Draw team names
    draw.text((200, 20), score_data['batting_team_name'], font=font_small, fill='white')
    draw.text((810, 20), score_data['bowling_team_name'], font=font_small, fill='white')

    # Draw player details
    draw.text((50, 50), f"> {score_data['batter_one']}:", font=font_medium, fill='white')
    draw.text((50, 85), f"   {score_data['batter_two']}:", font=font_medium, fill='white')
    draw.text((800, 65), f"{score_data['bowler']}:", font=font_medium, fill='white')

    draw.text((210, 50), f"{score_data['batter_one_score']['runs']} ({score_data['batter_one_score']['balls']})", font=font_medium, fill='white')
    draw.text((210, 85), f"{score_data['batter_two_score']['runs']} ({score_data['batter_two_score']['balls']})", font=font_medium, fill='white')
    draw.text((960, 65), f"{score_data['bowler_figure']['wickets']}-{score_data['bowler_figure']['runsGiven']}", font=font_medium, fill='white')

    # Draw score
    draw.text((500, 70), str(score_data['score']), font=font_large, fill='gold')
    draw.text((590, 65), str(score_data['overs_bowled']), font=font_medium, fill='gold')

    # Save the image to a BytesIO object
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr

# Usage
# image_data = create_score_strip(score_data)
# with open("score_strip.png", "wb") as f:
#     f.write(image_data)