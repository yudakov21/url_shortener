import './Button.css'

export default function Button({children, className, onClick}) {
    return <button className={className} onClick={onClick}> {children} </button>
}