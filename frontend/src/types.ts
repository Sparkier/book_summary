export interface Book {
	title: string;
	chapters: Chapter[];
	book_summary: string;
}

export interface SelectedImages {
	bookSelectedId: number;
	chapters: {
		chapterSelectedId: number;
		paragraphSelectedIds: number[];
	}[];
}

export interface Chapter {
	num: number;
	title: string;
	paragraphs: string[];
	paragraph_summaries: string[];
	chapter_summary: string;
}

export enum AbstractionLevel {
	BOOK = 'book',
	CHAPTER = 'chapter',
	PARAGRAPH = 'paragraph'
}

export enum ViewMode {
	IMAGE = 'image',
	TEXT = 'text',
	IMAGE_AND_TEXT = 'image+text'
}
