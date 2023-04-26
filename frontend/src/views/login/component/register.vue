<script setup lang="ts">
import { reactive, ref, watch, defineAsyncComponent } from 'vue';
import type { FormRules } from 'element-plus';
import { verifyEmail, verifyAccount, verifyPassword, verifyPhone } from '/@/utils/toolsValidate';
import { Iphone, Message } from '@element-plus/icons-vue';
import type { IRegisterMobileSchema, IRegisterSendCodeSchema, IRegisterEmailSchema } from '/@/api/login/register-api';
import { registerAPI } from '/@/api/login/register-api';
const countDownButton = defineAsyncComponent(() => import('/@/components/countDownButton/index.vue'));

const { registerMobileAPI, registerSendCodeAPI, registerEmailAPI } = registerAPI();
const FormRef = ref();

enum RegisterTypeEnum {
	Mobile = 'mobile',
	Email = 'email',
}

interface IFormSchema {
	username: string;
	password: string;
	email: string;
	mobile: string;
	code: string;
	register_type: RegisterTypeEnum;
}

interface IStateSchema {
	ruleForm: IFormSchema;
	rules: FormRules;
	isShowPassword: boolean;
}

// 定义变量内容
const state = reactive<IStateSchema>({
	ruleForm: {
		username: '',
		password: '',
		email: '',
		mobile: '',
		code: '',
		register_type: RegisterTypeEnum.Email,
	},
	rules: {
		username: [
			{ required: true, message: '请填写用户名', trigger: 'blur' },
			{
				validator: (rule: any, value: string, callback: Function) => {
					if (!verifyAccount(state.ruleForm.username)) {
						callback(new Error('字母开头，允许5-16字节，允许字母数字下划线'));
					} else {
						callback();
					}
				},
				trigger: 'blur',
			},
		],
		password: [
			{ required: true, message: '请填写密码', trigger: 'blur' },
			{
				validator: (rule: any, value: string, callback: Function) => {
					if (!verifyPassword(state.ruleForm.password)) {
						callback(new Error('以字母开头，长度在6~16之间，只能包含字母、数字和下划线'));
					} else {
						callback();
					}
				},
				trigger: 'blur',
			},
		],
		email: [
			{ required: true, message: '请填写邮箱', trigger: 'blur' },
			{
				validator: (rule: any, value: string, callback: Function) => {
					if (!verifyEmail(state.ruleForm.email)) {
						callback(new Error('请填写正确邮箱'));
					} else {
						callback();
					}
				},
				trigger: 'blur',
			},
		],
		mobile: [
			{ required: true, message: '请填写手机号', trigger: 'blur' },
			{
				validator: (rule: any, value: string, callback: Function) => {
					if (!verifyPhone(state.ruleForm.mobile)) {
						callback(new Error('请填写正确手机号'));
					} else {
						callback();
					}
				},
				trigger: 'blur',
			},
		],
	},
	isShowPassword: true,
});

const onRegister = async () => {
	console.log(state.ruleForm);
	if (!FormRef.value) return;
	await FormRef.value?.validate(async (valid: any) => {
		if (valid) {
			console.log(state.ruleForm);
			switch (state.ruleForm.register_type) {
				case RegisterTypeEnum.Email:
					await onRegisterEmail();
					break;
				case RegisterTypeEnum.Mobile:
					await onRegisterMobile();
					break;
				default:
					break;
			}
		}
	});
};

const onRegisterEmail = async () => {
	const payload: IRegisterEmailSchema = {
		username: state.ruleForm.username,
		password: state.ruleForm.password,
		email: state.ruleForm.email,
	};
	const { code, msg } = await registerEmailAPI(payload);
	console.log(code, msg);
};

const onRegisterMobile = async () => {
	const payload: IRegisterMobileSchema = {
		username: state.ruleForm.username,
		password: state.ruleForm.password,
		mobile: state.ruleForm.mobile,
		code: state.ruleForm.code,
	};
	const { code, msg } = await registerMobileAPI(payload);
	console.log(code, msg);
};

const onSendCode = async () => {
	const payload: IRegisterSendCodeSchema = { mobile: state.ruleForm.mobile };
	const { code, msg } = await registerSendCodeAPI(payload);
	console.log(code, msg);
};

watch(
	() => state.ruleForm.register_type,
	(val: RegisterTypeEnum) => {
		switch (val) {
			case RegisterTypeEnum.Email:
				state.ruleForm.mobile = '';
				state.ruleForm.code = '';
				break;
			case RegisterTypeEnum.Mobile:
				state.ruleForm.email = '';
				break;
			default:
				break;
		}
	}
);
</script>
<template>
	<el-form ref="FormRef" size="large" class="login-content-form" :model="state.ruleForm" :rules="state.rules">
		<el-form-item class="login-animation1" prop="username">
			<el-input text placeholder="请输入用户名" v-model="state.ruleForm.username" clearable autocomplete="off">
				<template #prefix>
					<el-icon class="el-input__icon"><ele-User /></el-icon>
				</template>
			</el-input>
		</el-form-item>
		<el-form-item class="login-animation2" prop="password">
			<el-input :type="state.isShowPassword ? 'text' : 'password'" placeholder="请输入密码" v-model="state.ruleForm.password" autocomplete="off">
				<template #prefix>
					<el-icon class="el-input__icon"><ele-Unlock /></el-icon>
				</template>
				<template #suffix>
					<i
						class="iconfont el-input__icon login-content-password"
						:class="state.isShowPassword ? 'icon-yincangmima' : 'icon-xianshimima'"
						@click="state.isShowPassword = !state.isShowPassword"
					>
					</i>
				</template>
			</el-input>
		</el-form-item>
		<el-form-item>
			<el-row class="w100">
				<el-col :span="19">
					<el-form-item v-if="state.ruleForm.register_type == RegisterTypeEnum.Email" class="login-animation1" prop="email">
						<el-input text placeholder="请输入邮箱" v-model="state.ruleForm.email" clearable autocomplete="off" class="w100">
							<template #prefix>
								<el-icon class="el-input__icon"><ele-Message /></el-icon>
							</template>
						</el-input>
					</el-form-item>
					<el-form-item v-if="state.ruleForm.register_type == RegisterTypeEnum.Mobile" class="login-animation1" prop="mobile">
						<el-input text placeholder="请输入手机号" v-model="state.ruleForm.mobile" clearable autocomplete="off" class="w100">
							<template #prefix>
								<i class="iconfont icon-dianhua el-input__icon"></i>
							</template>
						</el-input>
					</el-form-item>
				</el-col>
				<el-col :span="1"></el-col>
				<el-col :span="4">
					<el-button
						type="primary"
						class="w100"
						plain
						@click="
							state.ruleForm.register_type =
								state.ruleForm.register_type === RegisterTypeEnum.Email ? RegisterTypeEnum.Mobile : RegisterTypeEnum.Email
						"
					>
						<el-icon>
							<Iphone v-if="state.ruleForm.register_type == RegisterTypeEnum.Email" />
							<Message v-if="state.ruleForm.register_type == RegisterTypeEnum.Mobile" />
						</el-icon>
					</el-button>
				</el-col>
			</el-row>
		</el-form-item>
		<el-form-item v-show="state.ruleForm.register_type == RegisterTypeEnum.Mobile" class="login-animation2" prop="code">
			<el-col :span="15">
				<el-input text maxlength="6" placeholder="请输入验证码" v-model="state.ruleForm.code" clearable autocomplete="off">
					<template #prefix>
						<el-icon class="el-input__icon"><ele-Position /></el-icon>
					</template>
				</el-input>
			</el-col>
			<el-col :span="1"></el-col>
			<el-col :span="8">
				<countDownButton :disabled="state.ruleForm.mobile.length === 0" @send="onSendCode" />
			</el-col>
		</el-form-item>

		<el-form-item class="login-animation3">
			<el-button round type="primary" v-waves class="login-content-submit" @click="onRegister">
				<span>注 册</span>
			</el-button>
		</el-form-item>
	</el-form>
</template>

<style scoped lang="scss">
.login-content-form {
	margin-top: 20px;
	@for $i from 1 through 4 {
		.login-animation#{$i} {
			opacity: 0;
			animation-name: error-num;
			animation-duration: 0.5s;
			animation-fill-mode: forwards;
			animation-delay: calc($i/10) + s;
		}
	}
	.login-content-code {
		width: 100%;
		padding: 0;
	}
	.login-content-submit {
		width: 100%;
		letter-spacing: 2px;
		font-weight: 300;
		margin-top: 15px;
	}
	.login-msg {
		color: var(--el-text-color-placeholder);
	}
}
</style>
