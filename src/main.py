import requests
from xml_object import XMLObject
from converter import *

def main():

    # explanation: https://app.parlamento.pt/webutils/docs/doc.pdf?path=IIhbWadY8wbzqptPkj7rKbjz5BAixgBRPPu4hhM%2fHGEjzxbWQofGru18tscttPdtq5oZrDd4gQIzLf%2bNrrvCn%2bGPY9JWqHavazUl2CsdlFlrxvu8LdUvhrQ7Ve5io0vTthK3tQztX6GgURScc9tL1W6uuuuCrRiubpWIni%2fr2SXfMWvPpKcsqXdaibrBT6qFssARH4pIZmIpM%2bphmXr7FE2l6sNh6ga1HovAzpzQEzMCHdDSqrQ3tqlr56tbr%2bQPOzSk1ou%2bexUxwuD9oNR2CcMQXqc9tIQxQQrRLJmxzcdvdl0Kmxojxyz24Jm89XESAPuo%2bD8wly0MPpSLlxhz0lY%2f2JY11Cn0YLGkjtusmek%3d&fich=InformacaoBase.pdf&Inline=true 
    infobase_url = "https://app.parlamento.pt/webutils/docs/doc.xml?path=piH4nM%2bH4zC3Ukcy9%2bb3N%2bmcH0oYAE56Je3uDxPEBW%2bO0reHX0bvAVrEGlMyPQkTfWZYvEZZ6SomUrhduWVcLI13ioaXb36QHHnSNPzWorVAsfHTALh8dkXCsUhypC7ZXSHPneBWqrLU7Sm4G1GbgAUmdG9N%2fLqFyiQZ46J%2fmstGcS%2fwoP85b31Ivqya3JW7Dgc7X7yS2OCDOAFHgDO88qaqM1SbUl1pcr2UzcS%2fPtRrICm4vJwQ3VUcAgTUm7zVB8P007q1ZcZ7nePXgsZDQyufM26tP8ySahuBNDrYSQR%2bC8jwPO7D04CG%2bqJZyDgX%2brqVQ0sSwCkR31NubN36TKVG3hu6RHwTy1%2fp74VGcZ9IwLNXa2gnztxzHL%2bkfEjTuaO9DIY%2bXvGtp2G1gX%2fYTV4x5tM%2brPSpfv3%2bv%2bcTQyQ%3d&fich=InformacaoBaseXVII.xml&Inline=true"
    # explanation: https://app.parlamento.pt/webutils/docs/doc.pdf?path=rY7mVJGhWchhHKByeII%2fNqptrb14ViOTjWj2BtEPOX3NlX4Lie2C8x35u6txMaU0Q0LypVRRV25pVpevYxnQYI5RAFpTIVTCiS2WCkWzHw9wou%2fsCk1eqQ6OnXdETQTcoV55yuDaTc1TgvmY4TQPur5UQbUnMC0gRZtS%2f6S%2bWRsrqns566g%2fV2B327803lleohvVfEQJLLfo%2be5pUXP%2bLAOOOTa0Mlw%2fSg0nUdm3ixDbcYSXYxdG7WsFjiBSToq%2f3rY1aHxpZ6YxTI5S4LLZOmJhMwH9%2bShKQxUwZ50iJ8PtHAQJfQ3sty3fGg1LhoeiSY3OzTdxAOkJfogtyaFukhL4GlCFCGoQzCS4ke1dug7McaPpkv%2fL2TJn6Wd%2fwlNc&fich=RegistoBiografico.pdf&Inline=true
    interests_url = "https://app.parlamento.pt/webutils/docs/doc.xml?path=JmDHvUICxNGLsRcUSyKtqlqm6degQj012wUXS5kAbiyDtsP6eLJxEqFEbkKsnzF0v%2fiy3LLMxC7AFn5COXXJMf1bB3EhMQiCcbM5GzMGjLwRh5B9Hw07rUPAUeBnNwVh2QgZVa4bl6xvdWae%2bePrcOMNpNYVJC17xE1CxzX%2f3TfoZB0jDBv5O7kMxjghkY%2bJGqdwS%2b3rJ29sVJQYqb9zKxw56%2f14GRwdj8zfP1GZ0xUlqUDW40R6jFNw64YHto%2fdZI90ZEYS6gDrC0ugr6Kai9TmvLV0XHV403AlQubP3dCxjx4r%2bypASG9j%2b1r%2b%2bDbB6hZDy8dLuKxb7Gt1rIwQF5v8kz3gHQsDF1rQ36XZL%2bHq%2ftYGPOM2fTZhzXlWML7TaBd%2fRlo5r0b3g1zqx19mrw%3d%3d&fich=RegistoInteressesXVII.xml&Inline=true"

    response = requests.get(infobase_url)
    if response.status_code != 200:
        SystemExit("Failed to fetch data")

    # Remove BOM
    cleaned_data : str = XMLObject.remove_bom(response.text)

    xml_obj = XMLObject(cleaned_data)
    
    convert_to_rdf(xml_obj)

if __name__ == "__main__":
    main()
