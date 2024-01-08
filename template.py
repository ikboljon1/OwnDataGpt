template = """
Savol: {user_question}

# 1. Savol matnini tushunish
O'ylash: Foydalanuvchi {user_name} ning savoli "{user_question}" ekan.  
Uni diqqat bilan o'rganaman.

# 2. Tegishli javobni tanlash
{answering_logic}

# 3. Javobni yuborish
Yakuniy javob: 
{final_answer}
"""

answering_logic = """
Agar savol HoneyMoon tarkibi haqida bo'lsa, quyidagicha javob beraman: 

Javob matni:
HoneyMoon tarkibi quyidagi elementlarni o'z ichiga oladi: 
asal, bekmes, rayhon, galangal va hk.

Agar savol narxlari haqida bo'lsa, quyidagicha javob beraman:

Javob matni: 
HoneyMoon narxlari quyidagicha:
1 oyga - 300 ming so'm
2 oyga - 550 ming so'm 
3 oyga - 750 ming so'm
"""

final_answer = """  
Hurmatli {user_name}, sizning "{user_question}" degan savolingizga quyidagicha javob beraman: 

{answer}

Ko'proq ma'lumot uchun /info ni yuboring.
"""

# Template ni ishlatish

user_question = "honeymoon tarkibi nimalardan iborat?"
user_name = "John"

filled_template = template.format(
    user_question=user_question,
    user_name=user_name,
    answering_logic=answering_logic,
    final_answer=final_answer,
    answer = "Honeymoon tarkibi quyidagi elementlarni o'z ichiga oladi: asal, bekmes, rayhon, galangal va hk."
)

print(filled_template)
