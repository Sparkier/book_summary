import type { Book } from "./types";
export async function fetchBooks(): Promise<string[]> {
    const response = await fetch(`http://127.0.0.1:5000/api/get_books`);
    const jsonResponse = await response.json();
    const books = jsonResponse["books"] as string[];
    return books;
  }
  
  export async function fetchBook(book: string): Promise<Book> {
    return fetch(`http://127.0.0.1:5000/api/get_book/${book}`)
      .then((response) => response.json())
      .then((jsonResponse) => jsonResponse["book"] as Book);
  }