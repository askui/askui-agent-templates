import time
from askui import VisionAgent

with VisionAgent() as agent:
        agent.tools.webbrowser.open_new("https://www.miinto.com/men-shirts")
        time.sleep(5)
        extracted_products = []
    
        for _ in range(5):
            agent.mouse_scroll(0, -500)
            product = agent.get(
                'Extract only the product name and price in the format: {"name": "Product Name", "price": "$price"}. '
                'If no product is found, return null.'
            )
            if product:
                extracted_products.append(product)
                break
    

        with open("data.txt", "w", encoding="utf-8") as file:
           file.writelines(extracted_products)
