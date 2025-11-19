from_nameとto_urlをインプットとして、リダイレクトURLを返す最も簡単なフロントを実装して。

index.htmlに全て書いていい。

100行以内

--color-bg, --color-primary, --color-accentを共通化して扱い、AIっぽくないフラットデザイン

質素でOK.


curl -X 'POST' \
  'http://localhost:8000/shorten' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "from_name": "premierleague",
  "to_url": "https://www.premierleague.com/en"
}'

{
  "id": "2aa008c7-b8ae-484d-9b52-8b5d1eac3762",
  "from_name": "premierleague",
  "to_url": "https://www.premierleague.com/en",
  "count": 0
}
