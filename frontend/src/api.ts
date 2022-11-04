import type { Book } from "./types";
export async function fetchBooks(): Promise<string[]> {
  const response = await fetch(`/api/get_books`);
  const jsonResponse = await response.json();
  const books = jsonResponse["books"] as string[];
  return books;
}

export async function fetchBook(book: string): Promise<Book> {
  return fetch(`/api/get_book/${book}`)
    .then((response) => response.json())
    .then((jsonResponse) => jsonResponse["book"] as Book);
}
