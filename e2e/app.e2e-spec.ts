import { SearchtwoPage } from './app.po';

describe('searchtwo App', function() {
  let page: SearchtwoPage;

  beforeEach(() => {
    page = new SearchtwoPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
