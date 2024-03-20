import { PUBLIC_BACKEND_URL } from "$env/static/public";
import { error } from "@sveltejs/kit";

export async function load () {
    const response = await fetch(`${PUBLIC_BACKEND_URL}/api/books`);
        if (!response.ok) {
            error(500, "Could not fetch books.")
        }
    const books = await response.json()
        return { books }    
}