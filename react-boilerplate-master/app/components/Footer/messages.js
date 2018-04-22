/*
 * Footer Messages
 *
 * This contains all the text for the Footer component.
 */
import { defineMessages } from 'react-intl';

export default defineMessages({
  licenseMessage: {
    id: 'boilerplate.components.Footer.license.message',
    defaultMessage: 'EcoListen, parte de Cortech',
  },
  authorMessage: {
    id: 'boilerplate.components.Footer.author.message',
    defaultMessage: `
      {author} copyright
    `,
  },
  newMessage: {
    id: 'boilerplate.components.Footer.new.message',
    defaultMessage: `
      {author}
    `,
  },
});
