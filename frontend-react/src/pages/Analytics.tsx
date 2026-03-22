import { motion } from "framer-motion";

export default function Analytics() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <h1 className="text-3xl font-bold">Analytics</h1>
      <p className="text-gray-600 dark:text-gray-300">
        View insights, trends, and system behavior.
      </p>
    </motion.div>
  );
}