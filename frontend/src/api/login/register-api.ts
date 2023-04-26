import request from '/@/utils/request';

export interface IRegisterMobileSchema {
	username: string;
	password: string;
	mobile: string;
	code: string;
}

export interface IRegisterSendCodeSchema {
	mobile: string;
}

export interface IRegisterEmailSchema {
	username: string;
	password: string;
	email: string;
}

export function registerAPI() {
	return {
		/**
		 * 手机号注册
		 * @param data
		 * @returns
		 */
		registerMobileAPI: (data: IRegisterMobileSchema) => {
			return request({
				url: '/api/auth/register/mobile',
				method: 'post',
				data,
			});
		},
		/**
		 * 发送注册验证码
		 * @param params
		 * @returns
		 */
		registerSendCodeAPI: (params: IRegisterSendCodeSchema) => {
			return request({
				url: '/api/auth/register/send_code',
				method: 'get',
				params,
			});
		},
		/**
		 * 邮件注册
		 * @param data
		 * @returns
		 */
		registerEmailAPI: (data: IRegisterEmailSchema) => {
			return request({
				url: '/api/auth/register/email',
				method: 'post',
				data,
			});
		},
	};
}
