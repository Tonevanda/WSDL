import requests
from xml_object import XMLObject
from converter import *
from rdflib import *
from pyshacl import validate

def main():

    # explanation: https://app.parlamento.pt/webutils/docs/doc.pdf?path=IIhbWadY8wbzqptPkj7rKbjz5BAixgBRPPu4hhM%2fHGEjzxbWQofGru18tscttPdtq5oZrDd4gQIzLf%2bNrrvCn%2bGPY9JWqHavazUl2CsdlFlrxvu8LdUvhrQ7Ve5io0vTthK3tQztX6GgURScc9tL1W6uuuuCrRiubpWIni%2fr2SXfMWvPpKcsqXdaibrBT6qFssARH4pIZmIpM%2bphmXr7FE2l6sNh6ga1HovAzpzQEzMCHdDSqrQ3tqlr56tbr%2bQPOzSk1ou%2bexUxwuD9oNR2CcMQXqc9tIQxQQrRLJmxzcdvdl0Kmxojxyz24Jm89XESAPuo%2bD8wly0MPpSLlxhz0lY%2f2JY11Cn0YLGkjtusmek%3d&fich=InformacaoBase.pdf&Inline=true 
    infobase_XVII = "https://app.parlamento.pt/webutils/docs/doc.xml?path=piH4nM%2bH4zC3Ukcy9%2bb3N%2bmcH0oYAE56Je3uDxPEBW%2bO0reHX0bvAVrEGlMyPQkTfWZYvEZZ6SomUrhduWVcLI13ioaXb36QHHnSNPzWorVAsfHTALh8dkXCsUhypC7ZXSHPneBWqrLU7Sm4G1GbgAUmdG9N%2fLqFyiQZ46J%2fmstGcS%2fwoP85b31Ivqya3JW7Dgc7X7yS2OCDOAFHgDO88qaqM1SbUl1pcr2UzcS%2fPtRrICm4vJwQ3VUcAgTUm7zVB8P007q1ZcZ7nePXgsZDQyufM26tP8ySahuBNDrYSQR%2bC8jwPO7D04CG%2bqJZyDgX%2brqVQ0sSwCkR31NubN36TKVG3hu6RHwTy1%2fp74VGcZ9IwLNXa2gnztxzHL%2bkfEjTuaO9DIY%2bXvGtp2G1gX%2fYTV4x5tM%2brPSpfv3%2bv%2bcTQyQ%3d&fich=InformacaoBaseXVII.xml&Inline=true"
    infobase_XVI = "https://app.parlamento.pt/webutils/docs/doc.xml?path=q50lxFuC9L1BQ0ZDWxvA1UbNVskBZgNJ8%2fFurUs11fV3RINgo%2b52TwtZv%2fqqwh8KNfjAqnmS2siud%2bGSdETPjOKEGmY1pz0Mk8S0V8mg3bCSFQ3LzvQiD8hazSO6dOTElc6N5XTl3WTveQ7wjwIkPSd7Hgcvy9VV%2f8SEr5XlghT72DDkzVZejYvJ6%2fAeK7e4RDM3Tef3te2Kt88m5Vm5GEEY2r%2bM8PTaDStrOVJXiZl4nr5f1WTy0vzQzQGMUJlR8R6%2bA0tcYDoJ7pFIUZrE9l5MbDzT0X%2bSjCOdBVpfS%2fcIHP3t099Y3zb3rRDcwDXEMXN01mF83H36PUftL8Hp8umH5Xm6b%2fotUaIOg1H8C%2bM%3d&fich=InformacaoBaseXVI.xml&Inline=true"

    bio_XVII = "https://app.parlamento.pt/webutils/docs/doc.xml?path=OVrPwI%2b%2fRcb9l5PKAmHNPPUSkuQvGxH%2fX%2beFMaUjZAjdvGa0NtBwEQ0XKKCHMbfcCRVRQYGxCSJoZf1HSYWyz6lrbxgmDB4Cy%2bf%2bnmi8II5T%2fC2aoGrEXRE5EQ%2b5IsuwGNNVzUw2iXpI0mKJBIyXTgCtyGEqhiDerUvC3PK3cCm9GJJX2RGKVQsAIz2VZ4ACqufKgrl0fo%2bZaJNUSdVXg4BpW%2f3wwdO9H0uiA4KGvUCsqxRCQmvMlS5%2b8bKpixrZsRzPDI1xL6gN0P5dKo9AHHuoncwe3Nys9DcozCH%2fbqahZ%2f%2f4PEs3iw7B%2btb3bxGiMz1x8xePQFRI%2bihVy8NRWSg7ca9V17tiznH76zLR2YOs9d1vqV%2fFC3UlfF%2fqgfQBNVfJ3h18BzxdAZjqOIydxH3PD2itgVoBATcvuNodbqo%3d&fich=RegistoBiograficoXVII.xml&Inline=true"
    bio_XVI = "https://app.parlamento.pt/webutils/docs/doc.xml?path=bLEpTaLq0nMj92rNM8O5JyenCnOMol%2bj901knJ%2fAhkx9VXN7DS3Rz68hvH7LRs90zOm%2bYYMEMlfDqIyXnSD0G4HIlL16WbaZjflDmpwy4j7D5NTaB9ERTXSzmYz8Z70umCQqM0LbtIuqAkXKopX4rr4UmqVe4GJuVmSYyqjEPMD5EzCB3Z2XIRdGxVmtLCZXY5i42r73JT8M8XUZDk8YvRazjwBJvjXl9hQEyVU1gOPVpUH13khD9U07zuoLj2Urk5frxLbhYuA13BcRUK5nL3hA3D6tD0oTq7yfwfVleNONoCCnpROc%2bpIGS3OTRfLaVwoP1A6KeRXchFECdFca7ro5WE3GR9Xf3XygvKuygsU%2f8g0oAj6kB79aNWKP7nx7%2fS%2fWkZahU2LRb2KTQo3yIl%2fpF1DPBgB8%2fbAJSS77pM4%3d&fich=RegistoBiograficoXVI.xml&Inline=true"

    infourls = [infobase_XVII, infobase_XVI]
    bio_urls = [bio_XVII, bio_XVI]

    g = Graph()
    g.bind("poli", POLI)
    g.parse("../resources/poliontology.ttl", format="turtle")

    # Informação Base
    for url in infourls:
        response = requests.get(url)
        if response.status_code != 200:
            SystemExit("Failed to fetch data")

        # Remove BOM
        cleaned_data : str = XMLObject.remove_bom(response.text)

        xml_obj = XMLObject(cleaned_data)
        
        g = convert_infobase_to_rdf(xml_obj, g)
    
    # Registo Biográfico
    """
    for url in bio_urls:
        response = requests.get(url)
        if response.status_code != 200:
            SystemExit("Failed to fetch data")

        # Remove BOM
        cleaned_data : str = XMLObject.remove_bom(response.text)

        xml_obj = XMLObject(cleaned_data)
        
        g = convert_bio_to_rdf(xml_obj, g)
    """
    # Validate the graph
    _, _, results_text = validate(
        data_graph=g,
        shacl_graph=Graph().parse("../resources/shacl.ttl", format="turtle"),
    )
    print("Validation Results: \n", results_text)

    # Save the file
    g.serialize(destination="test.ttl", format="turtle")

if __name__ == "__main__":
    main()
