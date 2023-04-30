import request from '/@/utils/request';

/**
 * （不建议写成 request.post(xxx)，因为这样 post 时，无法 params 与 data 同时传参）
 *
 * 登录api接口集合
 * @method signInAccountAPI 用户登录
 * @method signOut 用户退出登录
 */
export function useLoginApi() {
	return {
		signInAccountAPI: (data: object) => {
			return request({
				url: '/api/auth/sign_in/account',
				method: 'post',
				data,
			});
		},
		signOut: (data: object) => {
			return request({
				url: '/user/signOut',
				method: 'post',
				data,
			});
		},
		userInfoAPI: (params: object) => {
			return request({
				url: '/user/signOut',
				method: 'get',
				params,
			});
		},
	};
}
