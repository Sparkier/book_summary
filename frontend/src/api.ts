import type { Book } from "./types";
export async function fetchBooks(): Promise<string[]> {
  return fetch(`/api/get_books`)
    .then((response) => response.json())
    .then((jsonResponse: Object) => jsonResponse["books"] as string[]);
}

export async function fetchBook(book: string): Promise<Book> {
  return fetch(`/api/get_book/${book}`)
    .then((response) => response.json())
    .then((jsonResponse: Object) => jsonResponse["book"] as Book);
}
