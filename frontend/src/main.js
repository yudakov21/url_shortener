export const API_BASE = "http://127.0.0.1:8000/";

export async function shortenUrl(longUrl) {
    const res = await fetch(`${API_BASE}`,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({long_url: longUrl})
    })

    if (!res.ok) {
        throw new Error("API error");
    }

    return await res.json()
}