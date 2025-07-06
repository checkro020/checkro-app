from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import re

PROHIBITED_RULES = {
    "P-01": {"desc": "Conteúdo adulto ou pornográfico", "terms": ["adulto", "pornô", "xxx"]},
    "P-02": {"desc": "Conteúdo violento ou chocante", "terms": ["violência", "sangue", "gore"]},
    "P-03": {"desc": "Discurso de ódio, discriminação ou assédio", "terms": ["ódio", "racismo", "discriminação"]},
    "P-04": {"desc": "Atividades ilegais", "terms": ["ilegal", "criminoso"]},
    "P-05": {"desc": "Drogas e substâncias proibidas", "terms": ["droga", "maconha", "cocaína"]},
    "P-06": {"desc": "Bebidas alcoólicas e tabaco", "terms": ["álcool", "cerveja", "tabaco"]},
    "P-07": {"desc": "Armas, munições e explosivos", "terms": ["arma", "pistola", "explosivo"]},
    "P-08": {"desc": "Conteúdo enganoso ou sensacionalista", "terms": ["milagre", "cura instantânea"]},
    "P-09": {"desc": "Fraudes e esquemas de dinheiro fácil", "terms": ["dinheiro fácil", "enriquecer rápido"]},
    "P-10": {"desc": "Clickbait excessivo", "terms": ["você não vai acreditar", "choquei"]},
    "P-11": {"desc": "Downloads ilegais", "terms": ["torrent", "download grátis"]},
    "P-12": {"desc": "Conteúdo com direitos autorais", "terms": ["copyright", "protegido por direitos"]},
    "P-13": {"desc": "Manipulação de tráfego e cliques", "terms": ["cliques automáticos", "bot de tráfego"]},
    "P-14": {"desc": "Conteúdo insuficiente ou de baixa qualidade", "terms": []},
    "P-15": {"desc": "Excesso de anúncios e pop-ups", "terms": ["popup", "anúncio intrusivo"]},
    "P-16": {"desc": "Erros graves de navegação", "terms": []},
    "P-17": {"desc": "Hacking, cracking ou invasão de sistemas", "terms": ["hack", "crack", "invasão"]},
    "P-18": {"desc": "Fake news e desinformação", "terms": ["notícia falsa", "desinformação"]},
    "P-19": {"desc": "Programas de afiliados sem valor agregado", "terms": ["afiliado", "sem valor"]},
    "P-20": {"desc": "Conteúdo automatizado de baixa qualidade", "terms": ["gerado automaticamente", "ia não revisada"]},
    "P-21": {"desc": "Conteúdo médico duvidoso", "terms": ["cura milagrosa", "tratamento não comprovado"]},
    "P-22": {"desc": "Sites copiados ou sem identidade própria", "terms": ["cópia", "plágio"]},
    "P-23": {"desc": "Conteúdo político ou eleitoral enganoso", "terms": ["propaganda enganosa", "fake eleitoral"]},
    "P-24": {"desc": "Idioma não suportado pelo AdSense", "terms": []},
    "P-25": {"desc": "Redirecionamentos enganosos", "terms": ["redirecionamento suspeito"]},
    "P-26": {"desc": "Propagação de malware, vírus ou phishing", "terms": ["malware", "phishing"]},
    "P-27": {"desc": "Venda de dados pessoais", "terms": ["vender dados", "dados pessoais"]},
    "P-28": {"desc": "Conteúdo relacionado a apostas e cassinos online", "terms": ["cassino", "aposta online"]},
    "P-29": {"desc": "Sites que promovem ódio contra indivíduos ou grupos", "terms": ["ataque pessoal", "preconceito"]},
    "P-30": {"desc": "Uso de técnicas de SEO Black Hat", "terms": ["black hat", "spam seo"]},
    "P-31": {"desc": "Conteúdo com incentivo a comportamentos prejudiciais", "terms": ["comportamento perigoso", "autolesão"]},
    "P-32": {"desc": "Falsificação de identidade ou informações", "terms": ["falsificação", "identidade falsa"]},
    "P-33": {"desc": "Venda ou distribuição de contas do Google AdSense", "terms": ["venda adsense", "conta adsense"]},
    "P-34": {"desc": "Criptomoedas ou investimentos de alto risco sem informações confiáveis", "terms": ["criptomoeda", "investimento arriscado"]},
    "P-35": {"desc": "Sites apenas para redirecionamento", "terms": ["redirecionamento puro"]}
}

ALLOWED_RULES = {
    "A-01": {"desc": "Conteúdo original e educativo", "terms": ["guia", "tutorial", "educação"]},
    "A-02": {"desc": "Revisão e análises honestas", "terms": ["análise", "revisão", "opinião"]},
    "A-03": {"desc": "Notícias relevantes e atualizadas", "terms": ["notícia", "atualidade"]},
    "A-04": {"desc": "Artigos com boa estrutura e profundidade", "terms": ["artigo detalhado", "profundidade"]},
    "A-05": {"desc": "Uso correto de títulos H1, H2, meta descrição", "terms": []},
    "A-06": {"desc": "Imagens com texto alternativo (ALT)", "terms": []},
    "A-07": {"desc": "Páginas institucionais (Sobre, Contato, Privacidade)", "terms": []},
    "A-08": {"desc": "Escrita clara e sem erros", "terms": []},
    "A-09": {"desc": "Design responsivo e boa experiência móvel", "terms": []},
    "A-10": {"desc": "Conteúdo atualizado regularmente", "terms": []}
}

def crawl_site(url):
    visited = set()
    pages = []
    
    def get_links(current_url):
        if current_url in visited:
            return
        visited.add(current_url)
        
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            pages.append(current_url)
            
            for link in soup.find_all('a', href=True):
                next_url = urljoin(current_url, link['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    get_links(next_url)
        except requests.RequestException:
            pass
    
    get_links(url)
    return pages

def analyze_page(page):
    issues = []
    try:
        response = requests.get(page, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        
        for rule_code, rule_data in PROHIBITED_RULES.items():
            for term in rule_data["terms"]:
                if term.lower() in text:
                    issues.append({
                        "rule_code": rule_code,
                        "desc": rule_data["desc"],
                        "term": term,
                        "suggestion": "Remover ou revisar o conteúdo"
                    })
                    break
        
        if not issues and not any(rule_data["terms"] for rule_data in PROHIBITED_RULES.values() if rule_code in ["P-14", "P-16", "P-24"]):
            issues.append({
                "rule_code": "P-14",
                "desc": "Conteúdo insuficiente ou de baixa qualidade",
                "term": None,
                "suggestion": "Adicionar mais conteúdo relevante"
            })
    except requests.RequestException:
        issues.append({
            "rule_code": "P-16",
            "desc": "Erro ao acessar a página",
            "term": None,
            "suggestion": "Verificar o link"
        })
    
    return issues
