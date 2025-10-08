import requests
from xml_object import XMLObject

def main():

    url = "https://app.parlamento.pt/webutils/docs/doc.xml?path=piH4nM%2bH4zC3Ukcy9%2bb3N%2bmcH0oYAE56Je3uDxPEBW%2bO0reHX0bvAVrEGlMyPQkTfWZYvEZZ6SomUrhduWVcLI13ioaXb36QHHnSNPzWorVAsfHTALh8dkXCsUhypC7ZXSHPneBWqrLU7Sm4G1GbgAUmdG9N%2fLqFyiQZ46J%2fmstGcS%2fwoP85b31Ivqya3JW7Dgc7X7yS2OCDOAFHgDO88qaqM1SbUl1pcr2UzcS%2fPtRrICm4vJwQ3VUcAgTUm7zVB8P007q1ZcZ7nePXgsZDQyufM26tP8ySahuBNDrYSQR%2bC8jwPO7D04CG%2bqJZyDgX%2brqVQ0sSwCkR31NubN36TKVG3hu6RHwTy1%2fp74VGcZ9IwLNXa2gnztxzHL%2bkfEjTuaO9DIY%2bXvGtp2G1gX%2fYTV4x5tM%2brPSpfv3%2bv%2bcTQyQ%3d&fich=InformacaoBaseXVII.xml&Inline=true"

    response = requests.get(url)
    if response.status_code != 200:
        SystemExit("Failed to fetch data")

    # Remove BOM
    cleaned_data = XMLObject.remove_bom(response.text)

    xml_obj = XMLObject(XMLObject.toTreeElement(cleaned_data), cleaned_data)

    print(xml_obj.get_string())


if __name__ == "__main__":
    main()
