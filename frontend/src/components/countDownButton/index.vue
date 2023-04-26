<template>
	<el-button v-waves class="login-content-code" :disabled="disabled || isDisabled" @click="onSendCode">
		{{ buttonText }}
	</el-button>
</template>

<script>
import { ref, watch, onUnmounted, defineComponent } from 'vue';

export default defineComponent({
	name: 'CountDownButton',
	props: {
		disabled: Boolean,
		sendButtonText: String,
		resendButtonText: String,
	},
	emits: ['send'],
	setup(props, { emit }) {
		const timerId = ref(null);
		const seconds = ref(60);
		const buttonText = ref(props.sendButtonText || '发送验证码');

		function onSendCode() {
			// 防止重复点击按钮
			if (seconds.value !== 60) {
				return;
			}
			buttonText.value = `${seconds.value} 秒后重发`;
			timerId.value = setInterval(() => {
				seconds.value--;
				if (seconds.value === 0) {
					seconds.value = 60;
					buttonText.value = props.sendButtonText || '发送验证码';
					clearInterval(timerId.value);
				} else {
					buttonText.value = `${seconds.value} 秒后重发`;
				}
			}, 1000);
			emit('send');
		}

		const isDisabled = ref(false);

		// 监听 seconds 的变化，更新 isDisabled 值
		watch(seconds, (newVal) => {
			isDisabled.value = newVal !== 60 || props.disabled;
		});

		// 组件销毁时清除定时器
		onUnmounted(() => {
			clearInterval(timerId.value);
		});

		return {
			buttonText,
			isDisabled,
			onSendCode,
		};
	},
});
</script>
