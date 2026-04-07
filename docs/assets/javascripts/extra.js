// Add breadcrumbs and related content to each page
document.addEventListener('DOMContentLoaded', function() {
  // Breadcrumbs implementation (WCAG 2.1 compliant)
  const createBreadcrumbs = () => {
    const article = document.querySelector('.md-content__inner');
    if (!article) return;

    // Get the current page title
    const pageTitle = document.querySelector('.md-content__inner h1')?.textContent || '';

    // Get the navigation path from the sidebar
    const activePage = document.querySelector('.md-nav__link--active');
    if (!activePage) return;

    // Build breadcrumb path by traversing up the navigation tree
    const breadcrumbItems = [];
    breadcrumbItems.push({ title: pageTitle, url: window.location.pathname });

    let parent = activePage.closest('.md-nav__item--nested');
    const visited = new Set();
    while (parent && !visited.has(parent)) {
      visited.add(parent);
      const link = parent.querySelector(':scope > .md-nav__link');
      if (link) {
        breadcrumbItems.unshift({
          title: link.textContent.trim(),
          url: link.getAttribute('href')
        });
      }
      parent = parent.parentElement?.closest('.md-nav__item--nested');
    }

    // Add home link at the beginning
    breadcrumbItems.unshift({ title: 'Home', url: '/' });

    // Create semantic breadcrumbs with <nav> landmark
    const breadcrumbsNav = document.createElement('nav');
    breadcrumbsNav.className = 'breadcrumbs';
    breadcrumbsNav.setAttribute('aria-label', 'Breadcrumb');

    const breadcrumbsList = document.createElement('ol');
    breadcrumbItems.forEach((item, index) => {
      const listItem = document.createElement('li');
      if (index < breadcrumbItems.length - 1) {
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        listItem.appendChild(link);
      } else {
        // Current page — mark with aria-current
        const currentSpan = document.createElement('span');
        currentSpan.setAttribute('aria-current', 'page');
        currentSpan.textContent = item.title;
        listItem.appendChild(currentSpan);
      }
      breadcrumbsList.appendChild(listItem);
    });

    breadcrumbsNav.appendChild(breadcrumbsList);

    // Insert breadcrumbs at the top of the article
    article.insertBefore(breadcrumbsNav, article.firstChild);
  };

  // Related content implementation (WCAG 2.1 compliant)
  const addRelatedContent = () => {
    const article = document.querySelector('.md-content__inner');
    if (!article) return;

    // Find sibling pages in navigation
    const currentNavItem = document.querySelector('.md-nav__link--active')?.parentElement;
    if (!currentNavItem) return;

    const navParent = currentNavItem.parentElement;
    if (!navParent) return;

    const siblings = Array.from(navParent.querySelectorAll(':scope > .md-nav__item > .md-nav__link'))
      .filter(link => !link.classList.contains('md-nav__link--active'))
      .slice(0, 4); // Limit to 4 related items

    if (siblings.length === 0) return;

    // Use <aside> with aria-labelledby for complementary landmark
    const relatedContent = document.createElement('aside');
    relatedContent.className = 'related-content';
    relatedContent.setAttribute('aria-labelledby', 'related-content-heading');

    const heading = document.createElement('h2');
    heading.id = 'related-content-heading';
    heading.textContent = 'Related Content';
    relatedContent.appendChild(heading);

    const list = document.createElement('ul');
    list.className = 'related-content-list';

    siblings.forEach(link => {
      const listItem = document.createElement('li');
      listItem.className = 'related-content-item';

      const relatedLink = document.createElement('a');
      relatedLink.className = 'related-content-link';
      relatedLink.href = link.getAttribute('href');
      relatedLink.textContent = link.textContent.trim();

      listItem.appendChild(relatedLink);
      list.appendChild(listItem);
    });

    relatedContent.appendChild(list);

    // Add to the end of the article
    article.appendChild(relatedContent);
  };

  // Execute functions with a slight delay to ensure DOM is fully processed
  setTimeout(() => {
    createBreadcrumbs();
    addRelatedContent();
  }, 100);
});
