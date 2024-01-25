from .items import DrugInfoItem


def extract_headers(iNode):
    name_of_drug = iNode.css("div#drug_header h1::text").get()

    drug_headers = iNode.css("div#drug_header div.DrugHeader__meta___B3BcU")
    headers = []
    for drug_header in drug_headers:
        title = drug_header.css("div.DrugHeader__meta-title___22zXC::text").get()
        if title.lower() == "marketer":
            marketer = drug_header.css(
                "div.DrugHeader__meta-value___vqYM0 a::text"
            ).get()
            headers.append(f"{title}: {marketer}")
        elif title.lower() == "salt composition":
            salt_composition = drug_header.css(
                "div.DrugHeader__meta-value___vqYM0 a::text"
            ).get()
            headers.append(f"{title}: {salt_composition}")
        else:
            storage = drug_header.css("div.DrugHeader__meta-value___vqYM0::text").get()
            headers.append(f"{title}: {storage}")

    content_str = "\n".join([f"- {x}" for x in headers])
    return {"title": name_of_drug, "content": content_str}


def extract_product_overview(iNode):
    title = iNode.css("h2::text").get()
    overview = iNode.css("div#overview div.DrugOverview__content___22ZBX::text").get()

    return {"title": title, "content": overview}


def extract_uses(iNode):
    title = iNode.css("h2::text").get()

    all_uses = []
    for li in iNode.css("li"):
        if li.css("span"):
            all_uses.append(li.css("span::text").get())
        else:
            all_uses.append(li.css("a::text").get())

    content_str = "\n".join([f"- {x}" for x in all_uses])
    return {"title": title, "content": content_str}


def extract_benefits(iNode):
    title = iNode.css("h2::text").get()
    all_benefits = []
    for node in iNode.css("div.ShowMoreArray__tile___2mFZk"):
        header = node.css("h3::text").get()
        desc = node.css("div::text").get()
        all_benefits.append(f"{header}: {desc}")

    content_str = "\n".join([f"- {x}" for x in all_benefits])
    return {"title": title, "content": content_str}


def extract_benefits_and_uses(iNode):
    innerNodes = iNode.css("div.DrugOverview__container___CqA8x")
    # assuming that first node will always be uses and second will be benefits
    all_uses = extract_uses(innerNodes[0])
    all_benefits = extract_benefits(innerNodes[1])

    return {"content": all_uses}


def extract_side_effects(iNode):
    title = iNode.css("h2::text").get()
    contentNodes = iNode.css(
        "div.DrugOverview__container___CqA8x>div.DrugOverview__content___22ZBX"
    )

    desc = contentNodes[0].css("div::text").get()
    side_effect_list = contentNodes[1].css("li::text").getall()

    side_effect_str = "\n".join([f"- {x}" for x in side_effect_list])

    return {
        "title": title,
        "content": f"{desc}\n{side_effect_str}",
    }


def extract_how_to_use(iNode):
    title = iNode.css("h2::text").get()
    content = iNode.css("div.DrugOverview__content___22ZBX::text").get()

    return {"title": title, "content": content}


def extract_how_drug_works(iNode):
    title = iNode.css("h2::text").get()
    content = iNode.css("div.DrugOverview__content___22ZBX::text").get()

    return {"title": title, "content": content}


def extract_safety_advice(iNode):
    title = iNode.css("h2::text").get()
    contentNodes = iNode.css("div.DrugOverview__content___22ZBX")
    catgs = contentNodes.css(
        "div.DrugOverview__warning-top___UD3xX span::text"
    ).getall()
    advices = contentNodes.css("div.DrugOverview__content___22ZBX::text").getall()

    content_str = "\n".join([f"- {x[0]}: {x[1]}" for x in zip(catgs, advices)])
    return {"title": title, "content": content_str}


def extract_missed_dose(iNode):
    title = iNode.css("h2::text").get()
    content_str = iNode.css("div.DrugOverview__content___22ZBX::text").get()

    return {"title": title, "content": content_str}


def extract_substitutes(iNode):
    pass


def extract_expert_advice(iNode):
    title = iNode.css("h2::text").get()

    all_advices = []
    for node in iNode.css("div.ExpertAdviceItem__content___1Djk2 li"):
        if node.css("div"):
            all_advices.append(node.css("div::text").get())
        else:
            all_advices.append(node.css("::text").get())

    content_str = "\n".join([f"- {x}" for x in all_advices])
    return {"title": title, "content": content_str}


def extract_fact_box(iNode):
    title = iNode.css("h2::text").get()
    all_facts = []
    for node in iNode.css("div.DrugFactBox__content___1417O>div"):
        left_text = node.css("div.DrugFactBox__col-left___znwNB::text").get()
        right_text = node.css("div.DrugFactBox__col-right___36e1P::text").get()
        all_facts.append(f"{left_text}: {right_text}")

    content_str = "\n".join([f"- {x}" for x in all_facts])

    return {"title": title, "content": content_str}


def extract_drug_interaction(iNode):
    title = iNode.css("h2::text").get()

    desc = iNode.css("div.DrugInteraction__desc___2y8bR::text").get()

    interactions = []
    for node in iNode.css(
        "div.DrugInteraction__content___1gXvf div.DrugInteraction__row___JxhfS"
    ):
        drug = node.css("div.DrugInteraction__drug___1XyzI span::text").get()
        brands = node.css("div.DrugInteraction__brands___2u2mM::text").getall()
        brand = " ".join(brands)
        interaction = node.css("div.DrugInteraction__interaction___nPIkU::text").get()
        interactions.append(f"{drug} from {brand} has {interaction}")

    content_str = desc + "\n" + "\n".join([f"- {x}" for x in interactions])

    return {"title": title, "content": content_str}


def extract_patient_concerns(iNode):
    pass


def extract_user_feedback(iNode):
    pass


def extract_faq(iNode):
    title = iNode.css("h2::text").get()

    questions = iNode.css("h3.Faqs__ques___1iPB9::text").getall()
    ans = iNode.css("div.Faqs__ans___1uuIW::text").getall()

    all_faqs = []
    for x in zip(questions, ans):
        all_faqs.append(f"{x[0]}\nAnswer: {x[1]}")

    content_str = "\n".join([f"- {x}" for x in all_faqs])

    return {"title": title, "content": content_str}


def extract(response):
    drug_item = DrugInfoItem()
    # with open("sample.html", "w", encoding="utf-8") as oFile:
    #     oFile.write(response.text)

    # get the drug headers
    drug_item["headers"] = extract_headers(response.css("div#drug_header"))

    drug_item["overview"] = extract_product_overview(response.css("div#overview"))

    innerNodes = response.css("div#uses_and_benefits").css(
        "div.DrugOverview__container___CqA8x"
    )
    # assuming that first node will always be uses and second will be benefits
    drug_item["uses"] = extract_uses(innerNodes[0])

    drug_item["benefits"] = extract_benefits(innerNodes[1])

    # drug_item["uses_n_benefits"] = extract_benefits_and_uses(
    #     response.css("div#uses_and_benefits")
    # )

    drug_item["side_effects"] = extract_side_effects(response.css("div#side_effects"))

    drug_item["how_to_use"] = extract_how_to_use(response.css("div#how_to_use"))

    drug_item["how_drug_works"] = extract_how_drug_works(
        response.css("div#how_drug_works")
    )

    drug_item["safety_advice"] = extract_safety_advice(
        response.css("div#safety_advice")
    )

    drug_item["missed_dose"] = extract_missed_dose(response.css("div#missed_dose"))

    # drug_item["substitutes"] = extract_substitutes(response.css("div#substitutes"))

    drug_item["expert_advice"] = extract_expert_advice(
        response.css("div#expert_advice")
    )
    drug_item["fact_box"] = extract_fact_box(response.css("div#fact_box"))

    if interactionNode := response.css("div#drug_interaction"):
        drug_item["drug_interaction"] = extract_drug_interaction(interactionNode)

    # drug_item["patient_concerns"] = extract_patient_concerns(
    #     response.css("div#patient_concerns")
    # )
    # drug_item["user_feedback"] = extract_user_feedback(
    #     response.css("div#user_feedback")
    # )
    drug_item["faq"] = extract_faq(response.css("div#faq"))

    return drug_item
