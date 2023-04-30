import { defineStore } from 'pinia';
import { Session } from '/@/utils/storage';
import { userAPI } from '/@/api/login/user-api';
const { userInfoAPI } = userAPI();
/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosState => ({
		userInfos: {
			username: '',
			avatar: '',
			time: 0,
			roles: [],
			authBtnList: [],
		},
	}),
	actions: {
		async setUserInfos() {
			// 存储用户信息到浏览器缓存
			if (Session.get('userInfo')) {
				this.userInfos = Session.get('userInfo');
			} else {
				const userInfos = <UserInfos>await this.getApiUserInfo();
				this.userInfos = userInfos;
			}
		},
		// 模拟接口数据
		// https://gitee.com/lyt-top/vue-next-admin/issues/I5F1HP
		async getApiUserInfo() {
			const { data } = await userInfoAPI({});
			data.roles = ['admin'];
			data.authBtnList = ['btn.add', 'btn.del', 'btn.edit', 'btn.link'];

			return data;
		},
	},
});
