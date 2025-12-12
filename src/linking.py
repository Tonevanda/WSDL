from rdflib import *

def get_electoral_circles_link(name: str) -> str | None:
    match(name):
        case "Europa":
            return "Q60160068"
        case "Fora da Europa":
            return "Q125549894"
        case "Portalegre":
            return "Q73218823"
        case "Bragança":
            return "Q60055008"
        case "Guarda":
            return "Q60184747"
        case "Évora":
            return "Q60055146"
        case "Beja":
            return "Q59573900"
        case "Castelo Branco":
            return "Q59848428"
        case "Açores":
            return "Q28679904"
        case "Viana do Castelo":
            return "Q60042025"
        case "Vila Real":
            return "Q60062631"
        case "Madeira":
            return "Q60053805"
        case "Viseu":
            return "Q60005179"
        case "Coimbra":
            return "Q60029746"
        case "Santarém":
            return "Q60049558"
        case "Faro":
            return "Q60035161"
        case "Leiria":
            return "Q59115317"
        case "Aveiro":
            return "Q59661572"
        case "Braga":
            return "Q60054028"
        case "Setúbal":
            return "Q58916101"
        case "Porto":
            return "Q59193855"
        case "Lisboa":
            return "Q43187878"
    return None
