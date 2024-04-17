import { PUBLIC_BACKEND_URL } from '$env/static/public';
export async function load({ params }) {
	const bookReq = await fetch(`${PUBLIC_BACKEND_URL}/api/books/${params.uuid}`);
	const metadataReq = await fetch(`${PUBLIC_BACKEND_URL}/api/books/${params.uuid}/metadata`);

	return {
		book: await bookReq.json(),
		metadata: await metadataReq.json(),
		id: params.uuid
	};
}
