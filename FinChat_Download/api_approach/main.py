import requests, json, base64, gzip, pandas as pd

if __name__ == "__main__":
    params = {
        'symbol': 'NSEI-RELIANCE',
    }

    response = requests.get(
        'https://finchat.io/_next/data/l7g1FjzPlR7xC8JhEtxNz/company/NSEI-RELIANCE.json',
            params=params
        )

    if response.status_code in {200, 201}:
        response = response.json()

        # with open("sample.json", "w") as f:
        #     json.dump(response, f, indent=4)
        # excel_data = base64.b64decode(response['pageProps']['data'])
        excel_data = gzip.decompress(bytes(response['pageProps']['data'], 'latin1'))
        excel_data = excel_data.decode('utf-8')
        excel_data = json.loads(excel_data)
        # print(json.dumps(excel_data, indent=4))
        with open("sample_decoded_data.json", "w") as f:
            json.dump(excel_data, f, indent=4)

        # df = pd.DataFrame(excel_data)

        # df.to_excel('sample.xlsx', index=False)

        # with open('sample.xlsx', 'wb') as f:
        #     f.write(bytes(response['pageProps']['data'], 'utf-16'))

    else:
        print(response.status_code, response.content)
