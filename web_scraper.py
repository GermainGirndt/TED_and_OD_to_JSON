import json
from requests_html import AsyncHTMLSession
from urllib.request import urlretrieve
import os

async_session = AsyncHTMLSession()

def get_ted_json(urls):

    

    TRANSCRIPT_ROUTE = '/transcript'
    LANGUAGE_QUERY = '?language=pt-br'

    def get_transcript(result):
        transcript = ""
        ps = result.html.find('p')
        for p in ps:
            transcript += p.text.replace("\n", "").replace("\t", "")
        return transcript

    async_functions = []
    
    for url in urls:
        async def get_ted_url( url=url):
            details = url + LANGUAGE_QUERY
            transcript = url + TRANSCRIPT_ROUTE + LANGUAGE_QUERY 
            details_response = await async_session.get(details)
            transcript_response = await async_session.get(transcript)
            return details_response, transcript_response
        async_functions.append(get_ted_url)

    results = async_session.run(*async_functions)

    all_data = []
    for result in results:
        print(result)
        details_response, transcript_response = result
        data = {}
        data["title"] = details_response.html.find('title', first=True).text
        data["type"] = "video"
        data["url"] = details_response.html.url
        data["body"] = get_transcript(transcript_response)
        all_data.append(data)
        print(data)
        print("-------------------------------------------------")
    
    for data in all_data:
        file_name = data["title"]
        with open(f'{file_name}.json', 'w') as outfile:
            json.dump(data, outfile)

def get_olhar_digital_json(urls):

    def get_text(result):
        transcript = ""
        text_div = result.html.find('div .mat-txt', first=True)

        ps = text_div.find('p')
        for p in ps:
            transcript += p.text.replace("\n", "").replace("\t", "")
        return transcript

    async_functions = []
    
    for url in urls:
        async def get_ted_url( url=url):
            response = await async_session.get(url)
            return response
        async_functions.append(get_ted_url)

    results = async_session.run(*async_functions)

    all_data = []
    for result in results:
        print(result)
        data = {}
        data["title"] = result.html.find('.mat-tit', first=True).text
        data["type"] = "article"
        data["url"] = result.html.url
        data["body"] = get_text(result)
        all_data.append(data)
    
    for data in all_data:
        file_name = data["title"]
        with open(f'{file_name}.json', 'w') as outfile:
            json.dump(data, outfile)

if __name__ == "__main__":
    ted_urls = [
        'https://www.ted.com/talks/helen_czerski_the_fascinating_physics_of_everyday_life',
        'https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution',
        'https://www.ted.com/talks/sarah_parcak_help_discover_ancient_ruins_before_it_s_too_late',
        'https://www.ted.com/talks/sylvain_duranton_how_humans_and_ai_can_work_together_to_create_better_businesses',
        'https://www.ted.com/talks/chieko_asakawa_how_new_technology_helps_blind_people_explore_the_world',
        'https://www.ted.com/talks/pierre_barreau_how_ai_could_compose_a_personalized_soundtrack_to_your_life',
        'https://www.ted.com/talks/tom_gruber_how_ai_can_enhance_our_memory_work_and_social_lives',
        'https://www.ted.com/talks/bruce_feiler_agile_programming_for_your_family',
        'https://www.ted.com/talks/kevin_kelly_how_technology_evolves',
        'https://www.ted.com/talks/poppy_crum_technology_that_knows_what_you_re_feeling',
        'https://www.ted.com/talks/blaise_aguera_y_arcas_how_computers_are_learning_to_be_creative',
        'https://www.ted.com/talks/oscar_schwartz_can_a_computer_write_poetry',
        'https://www.ted.com/talks/ray_kurzweil_get_ready_for_hybrid_thinking',
        'https://www.ted.com/talks/james_veitch_this_is_what_happens_when_you_reply_to_spam_email',
        'https://www.ted.com/talks/james_veitch_the_agony_of_trying_to_unsubscribe',
        'https://www.ted.com/talks/greg_gage_how_to_control_someone_else_s_arm_with_your_brain',
        'https://www.ted.com/talks/jane_mcgonigal_the_game_that_can_give_you_10_extra_years_of_life',
        'https://www.ted.com/talks/elon_musk_the_mind_behind_tesla_spacex_solarcity',
        'https://www.ted.com/talks/bill_gates_innovating_to_zero',
        'https://www.ted.com/talks/sherry_turkle_connected_but_alone',
        'https://www.ted.com/talks/martin_seligman_the_new_era_of_positive_psychology',
        'https://www.ted.com/talks/ramesh_raskar_imaging_at_a_trillion_frames_per_second',
        'https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux',
        'https://www.ted.com/talks/david_pogue_10_top_time_saving_tech_tips',
        'https://www.ted.com/talks/joseph_desimone_what_if_3d_printing_was_100x_faster',
        'https://www.ted.com/talks/kevin_slavin_how_algorithms_shape_our_world',
        'https://www.ted.com/talks/bettina_warburg_how_the_blockchain_will_radically_transform_the_economy',
        'https://www.ted.com/talks/tom_griffiths_3_ways_to_make_better_decisions_by_thinking_like_a_computer',
        'https://www.ted.com/talks/adam_alter_why_our_screens_make_us_less_happy',
        'https://www.ted.com/talks/alex_kipman_a_futuristic_vision_of_the_age_of_holograms'
    ]

    olhar_digital_urls = [
        'https://olhardigital.com.br/ciencia-e-espaco/noticia/nova-teoria-diz-que-passado-presente-e-futuro-coexistem/97786',
        'https://olhardigital.com.br/colunistas/wagner_sanchez/post/o_futuro_cada_vez_mais_perto/78972',
        'https://olhardigital.com.br/colunistas/wagner_sanchez/post/os_riscos_do_machine_learning/80584',
        'https://olhardigital.com.br/noticia/inteligencia-artificial-da-ibm-consegue-prever-cancer-de-mama/87030',
        'https://olhardigital.com.br/ciencia-e-espaco/noticia/inteligencia-artificial-ajuda-a-nasa-a-projetar-novos-trajes-espaciais/102772',
        'https://olhardigital.com.br/colunistas/jorge_vargas_neto/post/como_a_inteligencia_artificial_pode_mudar_o_cenario_de_oferta_de_credito/78999',
        'https://olhardigital.com.br/ciencia-e-espaco/noticia/cientistas-criam-programa-poderoso-que-aprimora-deteccao-de-galaxias/100683',
        'https://olhardigital.com.br/coronavirus/noticia/coronavirus-como-a-tecnologia-e-usada-para-combater-a-pandemia/98006',
        'https://olhardigital.com.br/noticia/mais-barata-tecnologia-de-transcricao-de-voz-comeca-a-mudar-o-mercado/91400',
        'https://olhardigital.com.br/video/ceos-de-gigantes-de-tecnologia-na-berlinda/104391',
        'https://olhardigital.com.br/video/as-doencas-fisicas-provocadas-pela-tecnologia/96839',
        'https://olhardigital.com.br/video/como-a-tecnologia-de-reconhecimento-facial-e-usada-mundo-afora/87181',
        'https://olhardigital.com.br/noticia/presidente-da-microsoft-lista-4-tecnologias-que-vao-definir-a-proxima-decada/92745',
        'https://olhardigital.com.br/coronavirus/noticia/como-executivos-do-setor-de-tecnologia-projetam-o-mundo-pos-pandemia/99756',
        'https://olhardigital.com.br/noticia/5g-entenda-o-que-e-e-o-que-pode-mudar-com-o-novo-padrao-de-internet-movel/77658',
        'https://olhardigital.com.br/video/lcd-oled-microled-entenda-as-diferencas-entre-as-telas/78693',
        'https://olhardigital.com.br/video/microled-a-nova-tecnologia-de-tela-que-promete-desbancar-o-oled/75501',
        'https://olhardigital.com.br/video/micro-led-entenda-a-tecnologia-que-deve-dominar-as-telas-nos-proximos-anos/82622',
        'https://olhardigital.com.br/video/nova-tela-tem-tecnologia-holografica/101363',
        'https://olhardigital.com.br/noticia/nova-tecnologia-pode-regenerar-tela-rachada-de-celular/49331',
        'https://olhardigital.com.br/noticia/xiaomi-implementa-tecnologia-otimiza-o-uso-de-bateria-e-as-oscilacoes-na-tela/85359',
        'https://olhardigital.com.br/dicas_e_tutoriais/noticia/veja-por-onde-comecar-na-hora-de-migrar-do-windows-para-o-linux/95120',
        'https://olhardigital.com.br/pro/noticia/criador-do-linux-eu-nao-sou-mais-um-programador/103351',
        'https://olhardigital.com.br/video/novas-tecnologias-deixam-o-mundo-mais-conectado/98424',
        'https://olhardigital.com.br/noticia/implante-conectado-diretamente-ao-cerebro-devolve-visao-a-cegos/96573',
    ]

    


    get_ted_json(ted_urls)
    get_olhar_digital_json(olhar_digital_urls)