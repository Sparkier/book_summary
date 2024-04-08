import type { Book, SelectedImages } from './types';

export async function fetchBooks(): Promise<string[]> {
	const response = await fetch(`/api/books`);
	const jsonResponse = (await response.json()) as { books: string[] };
	return jsonResponse['books'];
}

export async function fetchBook(book: string): Promise<Book> {
	const response = await fetch(`/api/books/${book}`);
	const jsonResponse = (await response.json()) as { book: Book };
	return jsonResponse['book'];
}

export async function fetchSelectedImages(book: string): Promise<SelectedImages> {
	const response = await fetch(`/api/books/${book}/images/selected`);
	const jsonResponse = await response.json();
	return jsonResponse as SelectedImages;
}
