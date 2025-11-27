import './App.css'
import { useState } from 'react'
import Button from './Button'
import { shortenUrl, API_BASE } from './main'


export default function Home() {
    const [query, setQuery] = useState("")
    const [slug, setSlug] = useState(null)

    async function handleShort(){
        const result = await shortenUrl(query)
        setSlug(result.data)
    }

    return (
        <div>
            <label htmlFor="name"> Long URL</label>
            <input type="text" id='name' className='control' value={query} onChange={(e) => setQuery(e.target.value)}/>
            <Button onClick={handleShort}> Shorten </Button>

            {slug && (
            <p>
                Short URL: <a href={`${API_BASE}${slug}`}> {API_BASE}{slug} </a>
            </p>
            )}  
        </div>
    )
}