import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideSocketIo, SocketIoConfig } from 'ngx-socket-io';
import { environment } from './environment/environment';
import {provideHttpClient} from '@angular/common/http';

const socketConfig: SocketIoConfig = {
  url: environment.apiUrL,
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    provideSocketIo(socketConfig),
  ]
};
