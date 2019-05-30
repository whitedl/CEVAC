import {NgModule} from '@angular/core';

import {
	MatSidenavModule,
	MatToolbarModule,
	MatIconModule,
	MatListModule,
	MatButtonModule,
	MatBadgeModule,
	MatExpansionModule
} from '@angular/material';

@NgModule({
	imports: [
		MatSidenavModule,
		MatToolbarModule,
		MatIconModule,
		MatListModule,
		MatButtonModule,
		MatBadgeModule,
		MatExpansionModule
	],
	exports: [
		MatSidenavModule,
		MatToolbarModule,
		MatIconModule,
		MatListModule,
		MatButtonModule,
		MatBadgeModule,
		MatExpansionModule
	]
})
export class MaterialModule {}