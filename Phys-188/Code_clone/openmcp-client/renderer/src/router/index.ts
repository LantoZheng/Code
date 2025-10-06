import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

const baseURL = import.meta.env.BASE_URL;

const routes: Array<RouteRecordRaw> = [
	{
		name : "default",
		path : "/",
		redirect : baseURL + "debug"
	},
	{
		path: baseURL + "debug",
		name: "debug",
		component: () => import( /* webpackMode: "eager" */ "@/views/debug/index.vue"),
		meta: { title: "Debug" }
	},
	{
		path: baseURL + "connect",
		name: "connect",
		component: () => import( /* webpackMode: "eager" */ "@/views/connect/index.vue"),
		meta: { title: "Connect" }
	},
	{
		path: baseURL + "setting",
		name: "setting",
		component: () => import( /* webpackMode: "eager" */ "@/views/setting/index.vue"),
		meta: { title: "Setting" }
	},
	{
		path: baseURL + "about",
		name: "about",
		component: () => import( /* webpackMode: "eager" */ "@/views/about/index.vue"),
		meta: { title: "Tools" }
	}
];

const router = createRouter({
	history: createWebHistory('/'),
	routes,
});


router.beforeEach((to, from, next) => {
	if (to.meta.title && document) {
		document.title = `OpenMCP | ${to.meta.title}`;
	}
	next();
});

export default router;