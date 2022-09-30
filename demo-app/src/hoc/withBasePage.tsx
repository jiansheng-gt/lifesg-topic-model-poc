import React from "react";
import { BasePage } from "src/components/BasePage";

export function withBasePage<Props extends React.Attributes>(WrappedComponent: React.ComponentType<Props>) {
	return (props: Props): JSX.Element => {
		return (
			<BasePage>
				<WrappedComponent {...props} />
			</BasePage>
		);
	}
}