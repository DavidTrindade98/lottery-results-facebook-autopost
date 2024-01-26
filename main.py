from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests
import io
import schedule

def Euromilhoes():
    url = 'https://www.euro-millions.com/pt/'
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    
    numeros = '     '.join([i.text for i in data.find_all("li", {"class": "resultBall ball"})])
    estrelas = '      '.join([x.text for x in data.find_all("li", {"class": "resultBall lucky-star"})])
    
    data_do_sorteio_finder = data.find("div", {"class": "innerPadding fx col jcen smOrder2"})
    data_do_sorteio_span = data_do_sorteio_finder.find("span")
    data_do_sorteio = data_do_sorteio_span.get_text().strip()

    return f"{data_do_sorteio}\n \n {numeros}\n \n {estrelas}"

def generate_image_with_text(text, background_image):
    image = Image.open(background_image)
    draw = ImageDraw.Draw(image)
    font_regular = ImageFont.truetype("./assets/Poppins-SemiBold.ttf", 120)
    font_semibold = ImageFont.truetype("./assets/Poppins-SemiBold.ttf", 80)

    text_bbox = draw.textbbox((0, 0), text, font=font_regular)

    text_x = (image.width - text_bbox[2]) // 2

    data_do_sorteio, numeros, estrelas = text.split('\n \n')
    
    data_do_sorteio_bbox = draw.textbbox((0, 0), data_do_sorteio, font=font_semibold)
    numeros_bbox = draw.textbbox((0, 0), numeros, font=font_regular)
    estrelas_bbox = draw.textbbox((0, 0), estrelas, font=font_regular)

    data_do_sorteio_x = text_x + (text_bbox[2] - data_do_sorteio_bbox[2]) // 2
    numeros_x = text_x + (text_bbox[2] - numeros_bbox[2]) // 2
    estrelas_x = text_x + (text_bbox[2] - estrelas_bbox[2]) // 2

    data_do_sorteio_y = 595 
    numeros_y = 960 
    estrelas_y = 1270

    data_do_sorteio_y += (text_bbox[3] - data_do_sorteio_bbox[3]) // 2
    numeros_y += (text_bbox[3] - numeros_bbox[3]) // 2
    estrelas_y += (text_bbox[3] - estrelas_bbox[3]) // 2

    draw.text((data_do_sorteio_x, data_do_sorteio_y), data_do_sorteio, font=font_semibold, fill=(0, 0, 0))
    draw.text((numeros_x, numeros_y), numeros, font=font_regular, fill=(0, 0, 0))
    draw.text((estrelas_x, estrelas_y), estrelas, font=font_regular, fill=(0, 0, 0))

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    return image_bytes

def post_message():
    page_id = '107174135785132'
    access_token = 'EAAYW7MVVAggBAEbdnQ1WX8eSuHlYExKBB9sSTtKO5J9c9yT0jimvXV7FeIU4FCFYN3l8pq86LhPrkc8ntscLtTf0Tpj40YyvsXT7MP8LLsEiqVAqhQwj6ppRmMpaDjqnIfxNaELdHGk2RXRjjzvnvpclYHitRHtrmiJLyL7Dw0tVFAdP2FZC71am2pJ4ZD'
    message = Euromilhoes()
    background_image_url = './/assets//euro-background.png'
    
    image_bytes = generate_image_with_text(message, background_image_url)
    
    post_url = f'https://graph.facebook.com/{page_id}/photos'
    
    payload = {
        'access_token': access_token
    }
    
    files = {
        'source': image_bytes
    }
    
    r = requests.post(post_url, data=payload, files=files)
    
    print(r.text)

# I replace this part bellow because the script was running on the Cpanel Cron Job Service to schedule and manage the Facebook posts.

#schedule.every().tuesday.at("22:00").do(post_message)
#schedule.every().friday.at("22:00").do(post_message)

#while True:
    #schedule.run_pending()



