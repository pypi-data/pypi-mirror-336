import requests
import urllib.parse
import os

def _gqlRequest(clientId, slug):
        gqlUrl = "https://gql.twitch.tv/gql"
        headers = {
            "Client-ID": clientId,
            "Content-Type": "application/json"
        }
        data = [{
            "operationName":"VideoAccessToken_Clip",
            "variables":{
                "platform":"web",
                "slug": slug},
            "extensions":{
                "persistedQuery":{
                    "version":1,
                    "sha256Hash":"6fd3af2b22989506269b9ac02dd87eb4a6688392d67d94e41a6886f1e9f5c00f"}}},
            {
            "operationName":"WatchTrackQuery",
            "variables":{
                "channelLogin":"stanz",
                "videoID":"null",
                "hasVideoID":"false"},
            "extensions":{
                "persistedQuery":{
                    "version":1,
                    "sha256Hash":"d8e507b720dd231780d57d325fb3a9bb8ee1ee60d424ae106e6dab328ea9b4c6"}}},
            {
            "operationName":"ChatClip",
            "variables":{
                "clipSlug":"GiantFuriousDolphinDxAbomb-mN3wSr_-cNuyED9T"},
            "extensions":{
                "persistedQuery":{
                    "version":1,
                    "sha256Hash":"9aa558e066a22227c5ef2c0a8fded3aaa57d35181ad15f63df25bff516253a90"}}}]
        response = requests.post(gqlUrl, json=data, headers=headers)
        try:
            json_response = response.json()
            clip_data = json_response[0]['data']['clip']
            sig = clip_data['playbackAccessToken']['signature']
            token = urllib.parse.quote(clip_data['playbackAccessToken']['value'])
            download_url = clip_data['videoQualities'][0]['sourceURL']
            return sig, token, download_url
        except Exception as e:
            raise RuntimeError("Failed to extract clip info from GQL response") from e

def downloadClip(clientId, url):
    signature, token, downloadURL = _gqlRequest(clientId, _decodeURL(url))
    response = requests.get(downloadURL + "?sig=" + signature + "&token=" + token, stream=True)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download clip. HTTP {response.status_code}: {response.text}")
    output_filename = "clip.mp4"
    output_path = os.path.join(os.getcwd(), output_filename)
    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

def _decodeURL(url):
    if "/clip/" in url:
        return url.split("/clip/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Twitch clip URL")