from sections.economy import QUESTIONS as ECONOMY
from sections.government import QUESTIONS as GOVERNMENT
from sections.society import QUESTIONS as SOCIETY
from sections.culture import QUESTIONS as CULTURE
SECTIONS=[("Economy",ECONOMY),("Government",GOVERNMENT),("Society",SOCIETY),("Culture",CULTURE)]
QUESTIONS=[q for _,s in SECTIONS for q in s]
assert len(QUESTIONS)==38
assert len({q["id"] for q in QUESTIONS})==38
