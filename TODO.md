Quando colocar um registro na table product, simultaneamente inserir na de history
Company route autualizar o modifed_at

# Depois das 18:00? Alguma hora do dia a data de registros modificados está ficando um dia a frente!
    
    # fuso_horario = timezone(timedelta(hours=-3))
    # d1 = datetime.now().astimezone(fuso_horario).strftime('%Y/%m/%d')