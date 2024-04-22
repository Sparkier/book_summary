import { PUBLIC_BACKEND_URL } from '$env/static/public';
import { error } from '@sveltejs/kit';

export async function load() {
	const response = await fetch(`${PUBLIC_BACKEND_URL}/api/books`);
	if (!response.ok) {
		throw error(response.status, { message: 'Could not load books' });
	}
	const books = await response.json();
	return { books };
}
