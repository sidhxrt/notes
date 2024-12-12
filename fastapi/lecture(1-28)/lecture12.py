# COOKIE & HEADER PARAMETERS -- LECTURE 12

from fastapi import FastAPI, Cookie, Header

app = FastAPI()

@app.get("/item")
async def read_items(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None),     #accept_encoding is a header parameter
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None)
):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "X-Token values": x_token    
    }


# even if accept_encoding is written like this, the Header() object will understand that it is talking about which header parameter and read it as Aceept-Encoding
# accept_encoding: str | None = Header(None, convert_underscores=False)
# this will not fetch the correct header parameter as we are disabling the ability of fastAPI to fetch correct header
# i.e it will not convert underscores to hyphens and thus Header() wont be able to recognize the required header parameter
# Header() will then be searching for exact header parameter 'accept_encoding'

# inspect element >> go to network >> check all available header parameters after a request has been made

