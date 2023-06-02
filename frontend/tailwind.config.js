/** @type {import('tailwindcss').Config} */

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				transparent: 'transparent'
			}
		}
	},
	fontFamily: {
		sans: ['-apple-system', 'BlinkMacSystemFont', 'Helvetica', 'sans-serif']
	},
	plugins: []
};
