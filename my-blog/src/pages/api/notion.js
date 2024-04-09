import Notion from 'notion-client';

const notion = new Notion();
notion.auth(process.env.NOTION_API_KEY);

export const getBlogPosts = async () => {
    const blogPostDb = await notion.getDatabase({
        id: process.env.NOTION_DATABASE_ID
    });
    const {results} = blogPostDb;
    return results;
}