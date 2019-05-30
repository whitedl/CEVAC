import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from 'src/app/app-routing.module';
import { AppComponent } from 'src/app/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MapviewComponent } from 'src/app/mapview/mapview.component';
import { MenusComponent } from 'src/app/menus/menus.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MaterialModule } from 'src/app/material.module';
import { AlertboxComponent } from 'src/app/alertbox/alertbox.component';

//for simulating api; remove for production
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService }  from 'src/app/in-memory-data.service';

@NgModule({
  declarations: [
    AppComponent,
    MapviewComponent,
    MenusComponent,
    AlertboxComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    MaterialModule,
	
    //remove when real api is ready
    HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false }
    )
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
