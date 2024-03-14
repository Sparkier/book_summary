import type { Book } from './types';

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
