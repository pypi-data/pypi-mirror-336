from ambientagi.services.agent_service import AmbientAgentService

# import json

# # Initialize the service
# service = AmbientAgentService()

# # Create an agent
# prompt = input("Describe your agent with a prompt: ")
# wallet_address = "0xbayoleems"
# response = service.create_agent(
#     prompt=prompt,
#     wallet_address=wallet_address,
# )
# print("AMBIENT AGENT CREATED!")
# print(json.dumps(response, indent=4))

# from ambientagi.services.agent_service import AmbientAgentService
# import os

# # Initialize the service
# twitter_service = AmbientAgentService().create_twitter_agent('f652e0b2-bbd0-48bd-a579-662e1c7120f5')
# twitter_service.update_twitter_credentials(
#     twitter_handle="@AmbientAgi_ai",
#     api_key=os.getenv("X_API_KEY"),
#     api_secret=os.getenv("X_API_SECRET"),
#     access_token=os.getenv("X_ACCESS_TOKEN"),
#     access_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
# )

# caption = input("Enter the caption for the tweet: ")
# path = input("Enter the path to the media file: ")
# media_type = input("Enter the media type (image or video): ")
# twitter_service.post_with_media(tweet_text=caption, media_path=path, media_type=media_type)
# import asyncio
# browser_service = AmbientAgentService().create_browser_agent('f652e0b2-bbd0-48bd-a579-662e1c7120f5')
# asyncio.run(browser_service.run_task('Fetch the latest news from the BBC website'))
# browser_service.get_page_content('https://www.google.com')

# firecrawl_agent = AmbientAgentService().create_firecrawl_agent('f652e0b2-bbd0-48bd-a579-662e1c7120f5')
# content = firecrawl_agent.scrape_website('https://etherscan.io/exportData?type=tokentxns&contract=0xeda8db2f0f8f00f0aedd6fdd756402ed86cd002f&a=&decimal=9')
# print(content['markdown'])

print("DEPLOY YOUR AGENT ON A BLOCKCHAIN NETWORK - ETHEREUM")
funder_private_key = input("Enter your private key: ")
amount_eth = input("Enter the amount of ETH to deploy: ")
token_name = input("Enter the name of the token: ")
symbol = input("Enter the symbol of the token: ")
image_path = input("Enter the path to the image of the token: ")

ethereum_agent = AmbientAgentService().add_blockchain(
    "f652e0b2-bbd0-48bd-a579-662e1c7120f5"
)
token_response = ethereum_agent.create_eth_token(
    privateKey="30fdd34373cc5d303e545df8ff32bceeee320825543e14abc63f1d43b0c3921a",
    token_name="Browsy",
    symbol="BRWSY",
    decimals=18,
    buy_value_eth=0.01,
    image_path="browsy.png",
)
print(token_response)
