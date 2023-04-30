import request from '/@/utils/request';

/**
 *
 * 用户api接口集合
 * @method userInfoAPI 用户信息
 */
export function userAPI() {
	return {
		userInfoAPI: (params: object) => {
			return request({
				url: '/api/auth/user/info',
				method: 'get',
				params,
			});
		},
	};
}
