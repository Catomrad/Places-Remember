import * as VKID from '@vkid/sdk';

    VKID.Config.set({
      app: APP_ID,
      redirectUrl: 'https://example.com'
    });


    const authButton = document.createElement('button');
    authButton.onclick = () => {
      VKID.Auth.login(); // После авторизации будет редирект на адрес, указанный в параметре redirect_uri
    };

    document.getElementById('container').appendChild(authButton);