# image_postprocessing.py

from PIL import Image, ImageDraw, ImageFont
from config import font_path

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return "\n".join(lines)

def add_margin_only(base_image_path, output_path, margin_top=200):
    img = Image.open(base_image_path)
    original_width, original_height = img.size
    margin_bottom = margin_top
    new_width = original_width
    new_height = original_height + margin_top + margin_bottom
    new_img = Image.new("RGBA", (new_width, new_height), "white")
    new_img.paste(img, (0, margin_top))
    new_img.save(output_path)

def add_bubble_text(base_image_path, json_data, output_path, margin_top=200, margin_bottom=200):
    img = Image.open(base_image_path)
    original_width, original_height = img.size
    new_width = original_width
    new_height = original_height + margin_top + margin_bottom
    new_img = Image.new("RGBA", (new_width, new_height), "white")
    new_img.paste(img, (0, margin_top))
    draw = ImageDraw.Draw(new_img)
    font_size = max(20, new_width // 40)
    font = ImageFont.truetype(str(font_path), font_size)
    
    dialogues = json_data.get("dialogues", [])
    caption = json_data.get("caption", "")
    dialogues = [d for d in dialogues if d.get("dialogue", "").strip()]
    if not dialogues:
        dialogues = [{"speaker": "", "dialogue": caption, "option": "narration"}]
    else:
        for d in dialogues:
            d["option"] = "normal" if d.get("speaker") else "narration"
    
    for idx, d in enumerate(dialogues):
        name = d["speaker"]
        text = d["dialogue"]
        option = d["option"]
        if option == "narration":
            full_text = text
        else:
            full_text = f"{name}: {text}"
        
        max_text_width = int(new_width * 0.8)
        wrapped_text = wrap_text(draw, full_text, font, max_text_width)
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        bubble_padding = 40
        if idx == 0:
            bubble_x1 = (new_width - text_width - 2 * bubble_padding) // 2
            bubble_y1 = margin_top - text_height - 40
            bubble_x2 = bubble_x1 + text_width + 2 * bubble_padding
            bubble_y2 = bubble_y1 + text_height + 2 * bubble_padding
        else:
            bubble_x1 = (new_width - text_width - 2 * bubble_padding) // 2
            bubble_y1 = margin_top + original_height + 30
            bubble_x2 = bubble_x1 + text_width + 2 * bubble_padding
            bubble_y2 = bubble_y1 + text_height + 2 * bubble_padding
        
        if option == "narration":
            draw.rounded_rectangle((bubble_x1, bubble_y1, bubble_x2, bubble_y2),
                                   radius=20, fill="white", outline="black", width=1)
        else:
            draw.ellipse((bubble_x1, bubble_y1, bubble_x2, bubble_y2),
                         fill="white", outline="black", width=1)
        
        text_x = bubble_x1 + bubble_padding
        text_y = bubble_y1 + bubble_padding
        draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill="black", spacing=10)
    
    new_img.save(output_path)
    print(f"✅ 말풍선이 추가된 이미지가 저장되었습니다: {output_path}")
